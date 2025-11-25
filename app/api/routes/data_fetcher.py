import asyncio

from fastapi import APIRouter
from app.schemas.data_fetcher import FetchArxivArticleRequest, FetchArxivArticleResponse
from app.core.data_fetcher import fetch_articles_by_query
from app.api.deps import TokenDep
from app.config import settings
from app.utils.db import SessionLocal, init_db
from app.utils.cruds import article_crud

from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_openai import ChatOpenAI


router = APIRouter()

embedder = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
        )
vector_store = Chroma(host=settings.CHROMA_DB_HOST, port=settings.CHROMA_DB_PORT,
    collection_name="demo",
    embedding_function=embedder,
)
llm = ChatOpenAI(
        base_url=settings.OPENAI_API_BASE,
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=0.5,
        disable_streaming=True,
    )

# Initialize database tables
init_db()
#

@router.post(
    "/fetch-arxiv-articles",
    response_model=FetchArxivArticleResponse,
    tags=["data-fetcher"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
def api_fetch_arxiv_articles(
    http_auth: TokenDep,  # JWT to be provided by IA-Parc  # noqa: ARG001
    body: FetchArxivArticleRequest,
) -> FetchArxivArticleResponse:
    
    fetched_articles: FetchArxivArticleResponse = asyncio.run(fetch_articles_by_query(body.query, body.max_results, body.sort_criterion))
    
    # Store articles in PostgreSQL database using CRUD operations
    db = SessionLocal()
    try:
        # Convert pydantic models to dict for bulk creation
        articles_data = [
            {
                "title": article.title,
                "summary": article.summary,
                "pdf_url": article.pdf_url,
                "published": article.published,
                "llm_summary": article.llm_summary
            }
            for article in fetched_articles.fetched_articles
        ]
        
        # Use bulk create with duplicate checking
        stored_articles = article_crud.bulk_create_articles(db, articles_data)
        print(f"Successfully stored {len(stored_articles)} new articles in database")
        
    except Exception as e:
        print(f"Error storing articles in database: {e}")
    finally:
        db.close()

    return fetched_articles