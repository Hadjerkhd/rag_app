from typing import List
import pandas as pd
import arxiv
from app.schemas.data_fetcher import Article, FetchArxivArticleResponse

async def fetch_articles_by_query(query:str="LLM",max_results:int=10,sort_criterion: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate ) -> FetchArxivArticleResponse:
  """search for articles in arxiv
  """
  articles : List[Article] = []

  client = arxiv.Client()

  search = arxiv.Search(
    query = query,
    max_results = max_results,
    sort_by =  arxiv.SortCriterion.SubmittedDate 
  )

  for r in client.results(search):
    article = Article(title=r.title, summary=r.summary, pdf_url=r.pdf_url,published=pd.to_datetime(r.published))
    articles.append(article)
  
  result: FetchArxivArticleResponse = FetchArxivArticleResponse(fetched_articles=articles)

  return result
