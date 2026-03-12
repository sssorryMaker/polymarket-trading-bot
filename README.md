# Polymarket Copy Trading Bot

A TypeScript bot that watches a target Polymarket wallet, detects trades in real time, and mirrors buy orders to your own account. Supports **EOA** and **proxy/safe** auth (signature types 0, 1, 2).

Inspired by [Building a Polymarket Copy Trading Bot \| QuickNode Guides](https://www.quicknode.com/guides/defi/polymarket-copy-trading-bot).

---

## Overview

- **Polymarket CLOB**: Your bot signs orders; the API handles order flow; settlement stays non-custodial on-chain (Polygon).
- **Data API (discovery)**: Finds new trades from the wallet you want to copy via REST polling.
- **WebSocket (optional)**: Faster market/user updates once subscribed.
- **Executor**: Sizes the copied order, runs checks, and submits it.
- **Risk & positions**: Tracks exposure and can block trades above your limits.
- **Demo guardrail**: By default the flow is **BUY-only** (SELL trades from the target are skipped).

---

## Prerequisites

- **Node.js** (v18+) and **npm**
- A funded wallet on **Polygon mainnet** with **USDC.e** and **POL** (for gas)
- **Polygon RPC URL** (e.g. [QuickNode](https://www.quicknode.com/) Polygon endpoint)
- The **Polymarket CLOB SDK** expects **ethers v5** (included in this project)

---

## Quick Start

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set at least:

- `TARGET_WALLET` — Polymarket wallet address to copy (`0x...`)
- `WALLET_PRIVATE_KEY` — Your wallet private key (`0x...`)
- `RPC_URL` — Polygon RPC URL (e.g. QuickNode)

For a small demo, use modest sizing (e.g. `MAX_TRADE_SIZE=5`, `POSITION_MULTIPLIER=0.1`).

### 3. Run the bot

```bash
npm start
```

On first run in EOA mode, the bot may trigger approval transactions for USDC.e/CTF spenders. Ensure the wallet has enough POL for gas.

---

## Architecture

| Component        | Role |
|-----------------|------|
| **TradeMonitor** | REST polling of Polymarket Data API to discover new trades from the target wallet. |
| **WebSocketMonitor** | Optional real-time updates via Polymarket `market` or `user` WebSocket channels. |
| **TradeExecutor** | Sizes copy trades, checks balance/allowance, places orders via CLOB client (FOK/FAK/LIMIT). |
| **PositionTracker** | Tracks positions from fills (in-memory; loaded/updated from successful copies). |
| **RiskManager** | Enforces session notional cap and per-market notional cap before execution. |

The main loop: detect trade → (if BUY) subscribe WS if needed → compute copy size → risk check → execute → record fill and stats.

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TARGET_WALLET` | Yes | Polymarket wallet address to copy (e.g. `0x...`). |
| `WALLET_PRIVATE_KEY` | Yes | Your wallet private key (0x-prefixed). |
| `RPC_URL` | Yes | Polygon RPC URL (e.g. QuickNode). |
| `SIG_TYPE` | No | Polymarket signature type. `0` = EOA (default), `1` = Poly Proxy, `2` = Poly Polymorphic. |
| `PROXY_WALLET_ADDRESS` | For 1/2 | Funder/proxy/safe address when using `SIG_TYPE=1` or `2`. Leave empty for EOA. |
| `POLYMARKET_GEO_TOKEN` | No | Geo token if provided by Polymarket for your region. |
| `POSITION_MULTIPLIER` | No | Copy size multiplier (default `0.1` = 10%). |
| `MAX_TRADE_SIZE` | No | Max copy trade size in USDC (default `100`). |
| `MIN_TRADE_SIZE` | No | Min copy trade size in USDC (default `1`). |
| `SLIPPAGE_TOLERANCE` | No | Slippage (default `0.02` = 2%). |
| `ORDER_TYPE` | No | `FOK`, `FAK`, or `LIMIT` (default `FOK`). |
| `USE_WEBSOCKET` | No | `true` / `false` (default `true`). |
| `USE_USER_CHANNEL` | No | Use user channel for WebSocket (default `false`). |
| `POLL_INTERVAL` | No | REST poll interval in ms (default `2000`). |
| `WS_ASSET_IDS` | No | Comma-separated asset IDs for market WebSocket. |
| `WS_MARKET_IDS` | No | Comma-separated market/condition IDs for user channel. |
| `MAX_SESSION_NOTIONAL` | No | Session notional cap in USDC; `0` = no cap. |
| `MAX_PER_MARKET_NOTIONAL` | No | Per-market notional cap; `0` = no cap. |
| `MIN_PRIORITY_FEE_GWEI` | No | Min priority fee for Polygon txs (default `30`). |
| `MIN_MAX_FEE_GWEI` | No | Min max fee for Polygon txs (default `60`). |

---

## Auth (SIG_TYPE and PROXY_WALLET_ADDRESS)

- **SIG_TYPE=0 (EOA)**  
  Default. Your signer is an EOA. Do not set `PROXY_WALLET_ADDRESS`. API credentials are derived or created from `WALLET_PRIVATE_KEY` at startup.

- **SIG_TYPE=1 (Poly Proxy)**  
  Set `PROXY_WALLET_ADDRESS` to your Polymarket proxy/safe address (funder).

- **SIG_TYPE=2 (Poly Polymorphic)**  
  Set `PROXY_WALLET_ADDRESS` to your polymorphic safe address (funder).

All CLOB usage (trader, `generate-api-creds`, `test-api-creds`) uses auth from config, driven by `SIG_TYPE` and `PROXY_WALLET_ADDRESS` in `.env`.

---

## Commands

| Command | Description |
|---------|-------------|
| `npm start` | Run the bot. |
| `npm run generate-api-creds` | Generate and write API credentials to `.polymarket-api-creds` (uses `SIG_TYPE` and `PROXY_WALLET_ADDRESS` from `.env`). |
| `npm run test-api-creds` | Validate static API credentials (same auth env vars). |
| `npm run build` | Compile TypeScript to `dist/`. |
| `npm run start:prod` | Run compiled `dist/index.js`. |

---

## Example output

**Startup:**

```
🤖 Polymarket Copy Trading Bot
================================
Target wallet: 0x...
Position multiplier: 10%
Max trade size: 100 USDC
Order type: FOK
WebSocket: Enabled
Auth: EOA (signature type 0)
================================

✅ Configuration validated
✅ Trader initialized
✅ WebSocket monitor initialized (market channel)
🚀 Bot started! Monitoring via: WebSocket + REST API
```

**When a BUY is detected and copied:**

```
🎯 NEW TRADE DETECTED
   Side: BUY YES
   Size: 12.5 USDC @ 0.620
   ...
📈 Executing copy trade (FOK): Copy notional: 1.25 USDC
✅ Successfully copied trade!
📊 Session Stats: 1/1 copied, 0 failed
```

**When a SELL is detected (skipped):**

```
⚠️  Skipping SELL trade (BUY-only safeguard enabled)
```

---

## Disclaimer

This code has **not** been audited. Use at your own risk. Audit any code before using real funds or deploying to production. Start with small sizes (e.g. `MAX_TRADE_SIZE=5` or lower) for testing.

---

## References

- [Building a Polymarket Copy Trading Bot \| QuickNode](https://www.quicknode.com/guides/defi/polymarket-copy-trading-bot)
- [Polymarket](https://polymarket.com/) — prediction markets on Polygon
- [Polymarket CLOB](https://github.com/Polymarket/clob-client) — order book client
