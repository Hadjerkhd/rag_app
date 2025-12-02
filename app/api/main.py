from fastapi import APIRouter

from app.api.routes import rag
from app.api.routes import data_fetcher

api_router = APIRouter()
api_router.include_router(rag.router)
api_router.include_router(data_fetcher.router)
