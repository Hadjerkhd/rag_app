import asyncio

from pathlib import Path
from fastapi import APIRouter
from app.models.data_fetcher import FetchArxivArticleRequest, FetchArxivArticleResponse
from app.core.data_fetcher import fetch_articles_by_query
from app.api.deps import TokenDep
from app.config import settings

from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_openai import ChatOpenAI


router = APIRouter()

embedder = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
        )
vector_store = Chroma(host=settings.DB_HOST, port=settings.DB_PORT,
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

    return fetched_articles