from loguru import logger
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_core.documents.base import Document

from app.schemas.data_fetcher import Article
from app.config import settings


async def retreive_context(question: str, vector_store: Chroma, top_k: int=5) -> Tuple[str, List[Document]]:
    logger.debug(f"Looking for similar context to the question {question}")
    results = vector_store.similarity_search(
    question,
    k=top_k)
    docs_content = "\n\n".join(doc.page_content for doc in results)
    return docs_content, results


async def index_document(doc: str, vectore_store: Chroma) -> int:
    # 1. Split text into Document objects
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.create_documents([doc])

    # Assign metadata (optional)
    for i, split in enumerate(splits):
        split.metadata = {
            "chunk_index": i,
            "source": "user_input",
            "length": len(split.page_content)
        }

    # add to Chroma
    vectore_store.add_documents(
        documents=splits,
    )

    return len(splits)



async def index_arxiv_document(article: Article, query: str, vectore_store: Chroma) -> int:
    # 1. Split text into Document objects
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNKS_SIZE,
        chunk_overlap=200
    )
    splits = text_splitter.create_documents([article.title+" "+article.summary])

    # Assign metadata (optional)
    for i, split in enumerate(splits):
        split.metadata = {
            "chunk_index": i,
            "source": query,
            "title":article.title,
            "URL": article.pdf_url,
            "length": len(split.page_content),
            "publication_date":str(article.published),
        }

    # add to Chroma
    vectore_store.add_documents(
        documents=splits,
    )

    return len(splits)

async def index_arxiv_articles(articles:list[Article],  query: str, vectore_store: Chroma):
    for article in articles:
        await index_arxiv_document(article,query,vectore_store)


async def retreive_arxiv_context(question: str, vector_store: Chroma, top_k: int = settings.TOP_K_RETRIEVE) -> Tuple[str, List[Document]]:
    logger.debug(f"Looking for similar context to the question {question}")

    results = vector_store.similarity_search_with_score(
        question,
        k=top_k
    )

    chunks = []
    docs = []

    for i, (doc, score) in enumerate(results, start=1):
        metadata = doc.metadata

        chunk = (
            f"[CHUNK_{i}]\n"
            f"Paper URL: {metadata.get('URL', 'N/A')}\n"
            f"Title: {metadata.get('title', 'N/A')}\n"
            f"Year: {str(metadata.get('publication_date', 'N/A'))}\n"
            f"Content: {doc.page_content}\n"
            f"Relevance Score: {round(score, 4)}"
        )
        chunks.append(chunk)
        docs.append(doc)

    formatted_context = (
        "<retrieved_chunks>\n"
        + "\n\n".join(chunks)
        + "\n</retrieved_chunks>"
    )

    return formatted_context, docs
#https://milvus.io/docs/how_to_enhance_your_rag.md