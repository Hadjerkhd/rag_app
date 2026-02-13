from pydantic import BaseModel
from app.schemas.data_fetcher import Article

class KG_triple(BaseModel):
    head: str
    relation: str
    tail: str

class KG_triples(BaseModel):
    triples: list[KG_triple]
    
class ConstructKBFromArticlesRequest(BaseModel):
    articles: list[Article]
    