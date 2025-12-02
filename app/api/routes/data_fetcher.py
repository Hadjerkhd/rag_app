import asyncio
import time

from fastapi import APIRouter
from app.schemas.data_fetcher import FetchArxivArticleRequest, FetchArxivArticleResponse
from app.core.data_fetcher import fetch_articles_by_query
from app.utils.db import SessionLocal, init_db
from app.utils.cruds import article_crud
from  app.schemas.data_fetcher import ArticleInDB

router = APIRouter()

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

@router.get(
    "/get-db-arxiv-articles",
    response_model=list[ArticleInDB],
    tags=["data-fetcher"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
def api_get_stored_arxiv_articles(
) -> list[ArticleInDB]:
    db = SessionLocal()
    try:
        articles = article_crud.get_articles(db=db, limit=100)    
        result = [ArticleInDB.model_validate(a) for a in articles]
        # Use bulk create with duplicate checking
        print("Successfully getting articles from database")
        
    except Exception as e:
        print(f"Error getting articles from database: {e}")
    finally:
        db.close()

    return result