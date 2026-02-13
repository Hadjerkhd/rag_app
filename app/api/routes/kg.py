import asyncio
import time

from fastapi import APIRouter
from app.schemas.data_fetcher import FetchArxivArticleRequest, FetchArxivArticleResponse
from app.core.kg import construct_KG_from_articles_list
from app.core.data_fetcher import fetch_articles_by_query
from app.utils.db import SessionLocal, init_db
from app.utils.cruds import article_crud
from  app.schemas.data_fetcher import ArticleInDB
from app.schemas.kg import KG_triples, ConstructKBFromArticlesRequest

router = APIRouter()

# Initialize database tables
# init_db()
# #

# @router.post(
#     "/contruct-kb",
#     response_model=KG_triples,
#     tags=["KG"],
#     responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
# )
# def api_contruct_kb_from_articles(
#     body: FetchArxivArticleRequest,
# ) -> ConstructKBFromArticlesRequest:
    
#     fetched_articles: FetchArxivArticleResponse = asyncio.run(fetch_articles_by_query(body.query, body.max_results, body.sort_criterion))
#         # Store articles in PostgreSQL database using CRUD operations
#     db = SessionLocal()
#     try:
#         # Convert pydantic models to dict for bulk creation
#         articles_data = [
#             {
#                 "title": article.title,
#                 "summary": article.summary,
#                 "pdf_url": article.pdf_url,
#                 "published": article.published,
#                 "llm_summary": article.llm_summary
#             }
#             for article in fetched_articles.fetched_articles
#         ]
        
#         # Use bulk create with duplicate checking
#         stored_articles = article_crud.bulk_create_articles(db, articles_data)
#         print(f"Successfully stored {len(stored_articles)} new articles in database")
        
#     except Exception as e:
#         print(f"Error storing articles in database: {e}")
#     finally:
#         db.close()
#     fetched_articles: FetchArxivArticleResponse = asyncio.run(construct_KG_from_articles_list(fetched_articles))
    
#     # Store articles in PostgreSQL database using CRUD operations
#     db = SessionLocal()
#     try:
#         # Convert pydantic models to dict for bulk creation
#         articles_data = [
#             {
#                 "title": article.title,
#                 "summary": article.summary,
#                 "pdf_url": article.pdf_url,
#                 "published": article.published,
#                 "llm_summary": article.llm_summary
#             }
#             for article in fetched_articles.fetched_articles
#         ]
        
#         # Use bulk create with duplicate checking
#         stored_articles = article_crud.bulk_create_articles(db, articles_data)
#         print(f"Successfully stored {len(stored_articles)} new articles in database")
        
#     except Exception as e:
#         print(f"Error storing articles in database: {e}")
#     finally:
#         db.close()

#     return fetched_articles