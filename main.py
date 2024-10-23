import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_bodyContent, 
    extract_bodyContent)

from parse import extract_with_ollama

st.title("Sports Stats AI Web Scraper")
url = st.text_input("Enter a sports Website URL: ")

if st.button("Scrape Website"):
    st.write("Scraping site")
    
    result = scrape_website(url)
    body_content = extract_bodyContent(result)
    cleaned_content = clean_bodyContent(body_content)

    st.session_state.dom_content = cleaned_content
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    extract_description = st.text_area("Enter what sport league you would like to extract stats from")

    if st.button("Extract Content"):
        if extract_description:
            st.write("Extracting Content")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = extract_with_ollama(dom_chunks, extract_description)
            st.write(result)
