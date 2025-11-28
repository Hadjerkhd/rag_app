# ui.py

import streamlit as st
import requests

API_URL = "http://fastapi_app:8000"
FETCH_ARTICLES_URL = "/fetch-arxiv-articles"
GET_DB_ARTICLES_URL = "/get-db-arxiv-articles"

def fetch_articles(keyword, max_articles):
    # Call the data_fetcher route to fetch articles from arXiv
    
    response = requests.post(
        url=f"{API_URL}{FETCH_ARTICLES_URL}",
        headers={"Content-Type": "application/json"},
        json={"query": keyword, "max_results": max_articles},
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch articles")
        return []
    
def get_db_articles():
    
    response = requests.get(
        url=f"{API_URL}{GET_DB_ARTICLES_URL}",
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get db articles")
        return []
    
def main():
    st.title("ArXiv Article Fetcher")

    # Input fields for keyword and max articles
    keyword = st.text_input("Enter a keyword:")
    max_articles = st.number_input(
        "Enter the maximum number of articles:", min_value=1, max_value=100, value=10
    )

    # Button to fetch articles
    if st.button("Fetch Articles"):
        articles = fetch_articles(keyword, max_articles)
        if articles:
            # Display articles in a table
            st.table(articles)
    st.title('DB articles')
    st.table(get_db_articles())


if __name__ == "__main__":
    main()
