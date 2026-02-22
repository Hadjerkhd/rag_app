import asyncio

from loguru import logger
from pathlib import Path
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from app.schemas.rag import AnswerToQuestion, QuestionForDocs, _parse_final_answer
from app.core.rag import retreive_context, index_document, retreive_arxiv_context
from app.core.vector_db import load_vector_store
from app.config import settings

from PyPDF2 import PdfReader

from langchain_openai import ChatOpenAI


router = APIRouter()

llm = ChatOpenAI(
        # base_url=settings.OPENAI_API_BASE,
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=0.5,
        streaming=True
    )
# Global variable to cache the vector store
_vector_store = None

def get_vector_store():
    """Lazy loader for the vector store to prevent startup race conditions."""
    global _vector_store
    if _vector_store is None:
        _vector_store = load_vector_store()
    return _vector_store

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

def get_system_prompt(question: str, context: str,file_name:str="answer.txt") -> str:
    """Load and format the system prompt from file."""
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / file_name
    prompt_template = prompt_path.read_text(encoding="utf-8")
    return prompt_template.format(question=question, context=context)


@router.post(
    "/answer-question",
    response_model=AnswerToQuestion,
    tags=["rag"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
async def api_answer_question(
    body: QuestionForDocs,
) -> AnswerToQuestion:
    answer: AnswerToQuestion

    logger.debug(f"Now going to retreive context for the question: {body.question}")
    joint_context, retreived_docs = await retreive_context(body.question,vector_store=get_vector_store())
    logger.debug(f"Retreived similar context to the question {joint_context}. \n Now, asking LLM to formulate the answer from this context")
    prompt = get_system_prompt(context=joint_context, question=body.question)
    response = await llm.ainvoke(prompt)
    llm_resposne = response.content
    answer = _parse_final_answer(llm_resposne)
    return answer


@router.post(
    "/answer-research-question",
    tags=["rag"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
async def api_answer_research_question(
    body: QuestionForDocs,
) -> StreamingResponse:
    
    async def stream_response():
        yield "🔍 Retrieving context from Arxiv...\n\n"
        logger.debug(f"Vector store loaded! \n Now going to retreive context for the question: {body.question}")
        
        joint_context, retreived_docs = await retreive_arxiv_context(body.question, vector_store=get_vector_store())
        
        yield "🧠 Asking LLM to formulate the answer...\n\n"
        logger.debug(f"Retreived similar context to the question. Now, asking LLM to formulate the answer")
        
        prompt = get_system_prompt(context=joint_context, question=body.question, file_name='researcher.txt')
        
        async for chunk in llm.astream(prompt):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(stream_response(), media_type="text/event-stream")

@router.post(
    "/index-doc",
    tags=["rag"],
    responses={500: {"description": "Internal server error"}, 400: {"description": "Bad request"}},
)
async def api_index_doc(
    file: UploadFile
) -> int:
    try:
        raw_text = extract_text_from_file(file)
        doc_len = await index_document(str(raw_text), get_vector_store())
        if doc_len:
            return doc_len
        else:
            raise Exception("Error while indexing document")
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        raise Exception("Error while indexing document")
