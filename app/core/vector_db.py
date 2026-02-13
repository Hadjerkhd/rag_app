from loguru import logger

from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from app.config import settings

def load_embeddings_model():
    logger.debug('Loading embeddin model')
    return SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
        )
def load_vector_store():
    embedder = load_embeddings_model()
    logger.debug("Loading Chroma vector store. This may take a while. Please wait. ")
    return Chroma(host=settings.CHROMA_DB_HOST, port=settings.CHROMA_DB_PORT,
    collection_name="demo",
    embedding_function=embedder,
)