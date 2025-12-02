import asyncio

from loguru import logger
from pathlib import Path
from fastapi import APIRouter
from fastapi import UploadFile
from app.schemas.rag import AnswerToQuestion, QuestionForDocs, _parse_final_answer
from app.core.rag import retreive_context, index_document
from app.config import settings

from PyPDF2 import PdfReader
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_openai import ChatOpenAI


router = APIRouter()

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

llm = ChatOpenAI(
        # base_url=settings.OPENAI_API_BASE,
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=0.5,
        disable_streaming=True,
    )
# --------- Helpers ---------

def extract_text_from_file(file: UploadFile) -> str | None:
    """Detect file type and extract raw text."""
    if file is not None and file.filename is not None:
        if file.filename.endswith(".txt"):
            return file.file.read().decode("utf-8")

        if file.filename.endswith(".pdf"):
            reader = PdfReader(file.file)
            return "\n".join([page.extract_text() for page in reader.pages])

        raise ValueError("Unsupported file type")
    else:
        raise ValueError("None existing file")
    return None

def get_system_prompt(question: str, context: str) -> str:
    """Load and format the system prompt from file."""
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "answer.txt"
    prompt_template = prompt_path.read_text(encoding="utf-8")
    return prompt_template.format(question=question, context=context)


@router.post(
    "/answer-question",
    response_model=AnswerToQuestion,
    tags=["rag"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
def api_answer_question(
    body: QuestionForDocs,
) -> AnswerToQuestion:
    answer: AnswerToQuestion
    
    vector_store = load_vector_store()
    logger.debug(f"Vector store loaded! \n Now going to retreive context for the question: {body.question}")
    joint_context, retreived_docs = asyncio.run(retreive_context(body.question,vector_store=vector_store))
    logger.debug(f"Retreived similar context to the question {joint_context}. \n Now, asking LLM to formulate the answer from this context")
    prompt = get_system_prompt(context=joint_context, question=body.question)
    answer = _parse_final_answer(llm.invoke(prompt).text())
    return answer


@router.post(
    "/index-doc",
    tags=["rag"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
def api_index_doc(
    file: UploadFile
) -> int:
    try:
        vector_store = load_vector_store()
        raw_text = extract_text_from_file(file)
        doc_len = asyncio.run(index_document(str(raw_text),vector_store))
        if doc_len:
            return doc_len
        else:
            raise Exception("Error while indexing document")
    except Exception:
        raise Exception("Error while indexing document")
