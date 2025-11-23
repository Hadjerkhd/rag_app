import os

from fastapi.routing import APIRoute
from fastapi_offline import FastAPIOffline

from app.api.main import api_router
from app.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return "-".join(str(tag) for tag in route.tags) + "-" + route.name


tags_metadata = [
    {
        "name": "rag",
        "description": "Retrieval augmented generation",
    },
]


# allow IAParc to configure root_path
ROOT_URL = os.getenv(key="ROOT_URL", default="")


description = """RAG API for Retrieval Augmented Generation.
"""


app = FastAPIOffline(
    title=settings.PROJECT_NAME,
    description=description,
    generate_unique_id_function=custom_generate_unique_id,
    openapi_tags=tags_metadata,
    root_path=ROOT_URL,
    static_url="/docs",
)

app.include_router(api_router)