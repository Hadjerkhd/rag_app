from loguru import logger
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_core.documents.base import Document



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

