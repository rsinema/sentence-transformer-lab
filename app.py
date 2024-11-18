# app.py
import streamlit as st
from typing import List
import requests

st.title("Ebook Vector Search")

# Search interface
query = st.text_input("Enter your search query:")
num_results = st.slider("Number of results", min_value=1, max_value=10, value=5)
search_type = st.radio("Search for:", ("Chunks of Text", "Books"))

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            try:
                response = requests.post(
                    "http://localhost:8000/api/search",
                    json={"text": query, "num_results": num_results, "books": search_type == "Books"}
                )
                results = response.json()
                
                if search_type == "Books":
                    for i, result in enumerate(results, 1):
                        with st.container():
                            st.markdown(f"### Result {i}")
                            st.markdown(f"**Title:** {result['title']}")
                            st.markdown(f"**Consine Similarity:** {result['similarity']:.2f}")
                else:
                    for i, result in enumerate(results, 1):
                        with st.container():
                            st.markdown(f"### Result {i}")
                            st.markdown(f"**Title:** {result['title']}")
                            st.markdown(f"**Consine Similarity:** {result['similarity']:.2f}")
                            st.markdown(f"**Text:** {result['text']}")
                            st.divider()
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please enter a search query")

# Optional: Add configuration section
with st.sidebar:
    st.header("Settings")
    st.markdown("""
    Configure your vector search settings here.
    
    Current endpoint: `http://localhost:8000/api/search`
    """)