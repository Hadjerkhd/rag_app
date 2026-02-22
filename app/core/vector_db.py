from loguru import logger
import chromadb
import time
from chromadb.config import Settings as ChromaSettings

from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from app.config import settings

def load_embeddings_model():
    logger.debug('Loading embedding model')
    return SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
        )

def load_vector_store():
    embedder = load_embeddings_model()
    logger.debug(f"Connecting to Chroma server at {settings.CHROMA_DB_HOST}:{settings.CHROMA_DB_PORT}...")
    
    # Explicitly use HttpClient for remote connections
    client = chromadb.HttpClient(
        host=settings.CHROMA_DB_HOST,
        port=settings.CHROMA_DB_PORT,
        settings=ChromaSettings(allow_reset=True)
    )

    # Wait for Chroma to be ready (retry mechanism)
    max_retries = 3
    for i in range(max_retries):
        try:
            client.heartbeat()
            logger.info("Successfully connected to Chroma server.")
            break
        except Exception as e:
            if i < max_retries - 1:
                logger.warning(f"Chroma server not ready yet (attempt {i+1}/{max_retries}). Retrying in 2 seconds...")
                time.sleep(2)
            else:
                logger.error("Could not connect to Chroma server after multiple attempts.")
                raise e

    return Chroma(
        client=client,
        collection_name="demo",
        embedding_function=embedder,
    )