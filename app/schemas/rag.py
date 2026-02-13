
from pydantic import BaseModel
from typing import Literal
import json

class AnswerToQuestion(BaseModel):
    answer: str
    relevant_context: str | None = None
    confidence: Literal["low", "medium", "high"] | None = None
    
class QuestionForDocs(BaseModel):
    question: str

def _parse_final_answer(message_content: str) -> AnswerToQuestion:
    try:
        json_snippet: str = "```".join(message_content.split("```json\n")[1].split("```")[:-1])
    except Exception:
        try:
            json_snippet = "```".join(message_content.split("```\n")[1].split("```")[:-1])
        except Exception:
            json_snippet = message_content
    final_answer = AnswerToQuestion(**json.loads(json_snippet))
    return final_answer
