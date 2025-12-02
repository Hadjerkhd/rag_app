import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "http://localhost:8000"
FETCH_ARTICLES_URL = "/fetch-arxiv-articles"
GET_DB_ARTICLES_URL = "/get-db-arxiv-articles"
CHAT_URL = "/chat"  # Add your RAG chat endpoint

# Page configuration
st.set_page_config(
    page_title="ArXiv RAG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .article-card {
        padding: 1.2rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: box-shadow 0.2s;
    }
    .article-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .article-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .article-meta {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .article-summary {
        font-size: 0.9rem;
        color: #444;
        line-height: 1.5;
    }
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        background-color: #fafafa;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: white;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        margin-right: 20%;
        border: 1px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'db_articles' not in st.session_state:
    st.session_state.db_articles = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

def fetch_articles(keyword, max_articles):
    """Fetch articles from arXiv"""
    try:
        response = requests.post(
            url=f"{API_URL}{FETCH_ARTICLES_URL}",
            headers={"Content-Type": "application/json"},
            json={"query": keyword, "max_results": max_articles},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['fetched_articles']
        else:
            st.error(f"Failed to fetch articles: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching articles: {str(e)}")
        return []

def get_db_articles():
    """Get articles from database"""
    try:
        response = requests.get(
            url=f"{API_URL}{GET_DB_ARTICLES_URL}",
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get database articles: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error getting database articles: {str(e)}")
        return []

def send_chat_message(message):
    """Send message to RAG chat endpoint"""
    try:
        response = requests.post(
            url=f"{API_URL}{CHAT_URL}",
            headers={"Content-Type": "application/json"},
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "No response received")
        else:
            return f"Error: Unable to get response (Status: {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

def display_article_card(article, index):
    """Display a single article in card format"""
    with st.container():
        st.markdown(f"""
            <div class="article-card">
                <div class="article-title">{index}. {article.get('title', 'No Title')}</div>
                <div class="article-meta">
                    <strong>Authors:</strong> {', '.join(article.get('authors', ['Unknown'])[:3])}
                    {f"et al." if len(article.get('authors', [])) > 3 else ""}<br>
                    <strong>Published:</strong> {article.get('published', 'Unknown')} | 
                    <strong>ID:</strong> {article.get('id', 'Unknown')}
                </div>
                <div class="article-summary">{article.get('summary', 'No summary available')[:300]}...</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("📄 View", key=f"view_{index}"):
                st.session_state[f"expanded_{index}"] = True
        with col2:
            if article.get('pdf_url'):
                st.link_button("📥 PDF", article['pdf_url'])
        
        if st.session_state.get(f"expanded_{index}", False):
            st.markdown(f"**Full Summary:**\n\n{article.get('summary', 'No summary available')}")
            if st.button("Hide", key=f"hide_{index}"):
                st.session_state[f"expanded_{index}"] = False

def main():
    # Header
    st.title("📚 ArXiv Research Assistant")
    st.markdown("Search, explore, and chat with ArXiv articles using AI")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Search Articles")
        keyword = st.text_input("Keyword:", placeholder="e.g., machine learning")
        max_articles = st.slider("Max Results:", min_value=5, max_value=50, value=10)
        
        if st.button("🔍 Search ArXiv", use_container_width=True):
            if keyword:
                with st.spinner("Fetching articles..."):
                    st.session_state.search_results = fetch_articles(keyword, max_articles)
                    st.success(f"Found {len(st.session_state.search_results)} articles!")
            else:
                st.warning("Please enter a keyword")
        
        st.divider()
        
        if st.button("🔄 Refresh Database", use_container_width=True):
            with st.spinner("Loading database articles..."):
                st.session_state.db_articles = get_db_articles()
                st.success(f"Loaded {len(st.session_state.db_articles)} articles from database")
        
        st.divider()
        st.caption("💡 Tip: Use the Chat tab to ask questions about the articles")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📋 Article Library", "🔍 Search Results"])
    
    # Tab 1: Chat Interface
    with tab1:
        st.header("Ask Questions About Articles")
        st.markdown("Chat with an AI assistant that can answer questions based on the article database.")
        
        # Chat container
        chat_container = st.container()
        with chat_container:
            # Display chat history
            for i, chat in enumerate(st.session_state.chat_history):
                if chat['role'] == 'user':
                    st.markdown(f'<div class="user-message"><strong>You:</strong><br>{chat["content"]}</div>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong><br>{chat["content"]}</div>', 
                              unsafe_allow_html=True)
        
        # Chat input
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                user_input = st.text_input("Your question:", 
                                          placeholder="e.g., What are the latest advances in transformers?",
                                          key="chat_input",
                                          label_visibility="collapsed")
            with col2:
                send_button = st.button("Send", use_container_width=True)
        
        if send_button and user_input:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Get AI response
            with st.spinner("Thinking..."):
                response = send_chat_message(user_input)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
            
            st.rerun()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Tab 2: Database Articles
    with tab2:
        st.header("Article Library")
        st.markdown("Browse all articles stored in the database")
        
        if st.session_state.db_articles is None:
            st.info("👈 Click 'Refresh Database' in the sidebar to load articles")
        elif len(st.session_state.db_articles) == 0:
            st.warning("No articles found in database")
        else:
            # Filter options
            col1, col2 = st.columns([3, 1])
            with col1:
                filter_text = st.text_input("Filter by title or author:", 
                                           placeholder="Type to filter...")
            with col2:
                st.metric("Total Articles", len(st.session_state.db_articles))
            
            # Filter articles
            filtered_articles = st.session_state.db_articles
            if filter_text:
                filtered_articles = [
                    a for a in st.session_state.db_articles 
                    if filter_text.lower() in a.get('title', '').lower() or
                       any(filter_text.lower() in author.lower() 
                           for author in a.get('authors', []))
                ]
            
            st.markdown(f"Showing {len(filtered_articles)} articles")
            
            # Display articles
            for idx, article in enumerate(filtered_articles, 1):
                display_article_card(article, idx)
    
    # Tab 3: Search Results
    with tab3:
        st.header("Search Results")
        
        if st.session_state.search_results is None:
            st.info("👈 Use the sidebar to search for articles")
        elif len(st.session_state.search_results) == 0:
            st.warning("No search results found")
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{len(st.session_state.search_results)} results found**")
            with col2:
                if st.button("Save to Database"):
                    st.success("Articles saved! (Implement save endpoint)")
            
            # Display search results
            for idx, article in enumerate(st.session_state.search_results, 1):
                display_article_card(article, idx)

if __name__ == "__main__":
    main()