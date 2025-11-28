from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime
from uuid import UUID


class Article(BaseModel):
    """article class
    """
    title: str
    summary: str
    pdf_url: str
    published: datetime
    llm_summary: str| None= None

class ArticleInDB(Article):
    id: UUID

    class Config:
        from_attributes = True 
        
        
class FetchArxivArticleResponse(BaseModel):
    fetched_articles: List[Article]
    
class FetchArxivArticleRequest(BaseModel):
    query: str
    max_results: int =10
    sort_criterion: Literal["SubmittedDate", "LastUpdatedDate", "Relevance"] = "SubmittedDate"
    