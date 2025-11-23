import asyncio

from pathlib import Path
from fastapi import APIRouter
from fastapi import UploadFile
from app.models.rag import AnswerToQuestion, QuestionForDocs, _parse_final_answer
from app.api.deps import TokenDep
from app.core.rag import retreive_context, index_document
from app.config import settings

from PyPDF2 import PdfReader
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
    http_auth: TokenDep,  # JWT to be provided by IA-Parc  # noqa: ARG001
    body: QuestionForDocs,
) -> AnswerToQuestion:
    answer: AnswerToQuestion
    
    joint_context, retreived_docs = asyncio.run(retreive_context(body.question,vector_store=vector_store))
    prompt = get_system_prompt(context=joint_context, question=body.question)
    answer = _parse_final_answer(llm.invoke(prompt).text())
    return answer


@router.post(
    "/index-doc",
    tags=["rag"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
def api_index_doc(
    http_auth: TokenDep,
    file: UploadFile
) -> int:
    try:
        raw_text = extract_text_from_file(file)
        doc_len = asyncio.run(index_document(str(raw_text),vector_store))
        if doc_len:
            return doc_len
        else:
            raise Exception("Error while indexing document")
    except Exception:
        raise Exception("Error while indexing document")
