from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


class Article(BaseModel):
    """article class
    """
    title: str
    summary: str
    pdf_url: str
    published: datetime
    llm_summary: str| None= None

class FetchArxivArticleResponse(BaseModel):
    fetched_articles: List[Article]
    
class FetchArxivArticleRequest(BaseModel):
    query: str
    max_results: int =10
    sort_criterion: Literal["SubmittedDate", "LastUpdatedDate", "Relevance"] = "SubmittedDate"