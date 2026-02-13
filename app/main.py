import os
import threading

from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi_offline import FastAPIOffline

from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

from app.api.main import api_router
from app.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return "-".join(str(tag) for tag in route.tags) + "-" + route.name


tags_metadata = [
    {
        "name": "rag",
        "description": "Retrieval augmented generation",
        
    },
    {
        "name": "data-fetcher",
        "description": "Fetcher for data from arxiv",
        
    },
]


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ui"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_tracing_with_timeout(timeout: int = 2) -> None:
    done = False

    def init() -> None:
        nonlocal done
        try:
            phoenix_tracer_provider = register(
                project_name="rag",
                batch=True,
                set_global_tracer_provider=False,
                endpoint=settings.COLLECTOR_ENDPOINT,
            )
            LangChainInstrumentor().instrument(tracer_provider=phoenix_tracer_provider)
            print("Phoenix tracing enabled.")
        except Exception as e:
            print(f"Phoenix tracing failed: {e}")
        finally:
            done = True

    t = threading.Thread(target=init)
    t.daemon = True
    t.start()

    # If not done in X seconds, give up silently
    t.join(timeout)
    if not done:
        print("Phoenix server not reachable → skipping tracing (timed out).")

init_tracing_with_timeout()
