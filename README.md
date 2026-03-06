# Polymarket Copy Trading Bot

Copies trades from a target Polymarket wallet to your own account. Supports EOA and proxy/safe auth (signature types 0, 1, 2).

## Setup

1. Copy `.env.example` to `.env` and fill in values.
2. Required: `TARGET_WALLET`, `PRIVATE_KEY`, `RPC_URL`.
3. For proxy/safe: set `SIG_TYPE` to `1` or `2` and set `PROXY_WALLET_ADDRESS` to your proxy/safe address.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TARGET_WALLET` | Yes | Polymarket wallet address to copy (e.g. `0x...`). |
| `PRIVATE_KEY` | Yes | Your wallet private key (0x-prefixed). |
| `RPC_URL` | Yes | Polygon RPC URL (e.g. QuickNode). |
| `SIG_TYPE` | No | Polymarket signature type. `0` = EOA (default), `1` = Poly Proxy, `2` = Poly Polymorphic. |
| `PROXY_WALLET_ADDRESS` | For 1/2 | Funder/proxy/safe address when using `SIG_TYPE=1` or `SIG_TYPE=2`. Leave empty for EOA. |
| `POLYMARKET_GEO_TOKEN` | No | Geo token if provided by Polymarket for your region. |
| `POSITION_MULTIPLIER` | No | Copy size multiplier (default `0.1` = 10%). |
| `MAX_TRADE_SIZE` | No | Max trade size in USDC (default `100`). |
| `MIN_TRADE_SIZE` | No | Min trade size in USDC (default `1`). |
| `SLIPPAGE_TOLERANCE` | No | Slippage (default `0.02` = 2%). |
| `ORDER_TYPE` | No | `FOK`, `FAK`, or `LIMIT` (default `FOK`). |
| `USE_WEBSOCKET` | No | `true`/`false` (default `true`). |
| `USE_USER_CHANNEL` | No | Use user channel for WebSocket (default `false`). |
| `WS_ASSET_IDS` | No | Comma-separated asset IDs for market WS. |
| `WS_MARKET_IDS` | No | Comma-separated market/condition IDs for user channel. |
| `MAX_SESSION_NOTIONAL` | No | Session notional cap in USDC; `0` = no cap. |
| `MAX_PER_MARKET_NOTIONAL` | No | Per-market notional cap; `0` = no cap. |
| `MIN_PRIORITY_FEE_GWEI` | No | Min priority fee (default `30`). |
| `MIN_MAX_FEE_GWEI` | No | Min max fee (default `60`). |

## Commands

- `npm start` — run the bot.
- `npm run generate-api-creds` — generate and write API credentials to `.polymarket-api-creds` (uses `SIG_TYPE` and `PROXY_WALLET_ADDRESS` from `.env`).
- `npm run test-api-creds` — validate static API credentials (uses same auth env vars).

## Auth (SIG_TYPE and PROXY_WALLET_ADDRESS)

- **SIG_TYPE=0 (EOA)**  
  Default. Your signer is an EOA. Do not set `PROXY_WALLET_ADDRESS`.

- **SIG_TYPE=1 (Poly Proxy)**  
  Set `PROXY_WALLET_ADDRESS` to your Polymarket proxy/safe address (funder).

- **SIG_TYPE=2 (Poly Polymorphic)**  
  Set `PROXY_WALLET_ADDRESS` to your polymorphic safe address (funder).

All CLOB client usage (trader, generate-api-creds, test-api-creds) reads auth from `config.auth`, which is driven by `SIG_TYPE` and `PROXY_WALLET_ADDRESS` in `.env`.
