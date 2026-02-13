import asyncio

from fastapi import APIRouter
from app.core.rag import index_arxiv_articles
from app.schemas.data_fetcher import ArticleInDB, FetchArxivArticleRequest, FetchArxivArticleResponse
from app.core.data_fetcher import fetch_articles_by_query, get_articles_from_db, store_articles_into_db
from app.utils.db import init_db
from app.core.vector_db import load_vector_store

router = APIRouter()

init_db()
chroma = load_vector_store()

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
    asyncio.run(store_articles_into_db(fetched_articles.fetched_articles))
    asyncio.run(index_arxiv_articles(fetched_articles.fetched_articles,query=body.query,vectore_store=chroma))
    return fetched_articles

@router.get(
    "/get-db-arxiv-articles",
    response_model=list[ArticleInDB],
    tags=["data-fetcher"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
def api_get_stored_arxiv_articles(
) -> list[ArticleInDB]:
   
    result = asyncio.run(get_articles_from_db())

    return result