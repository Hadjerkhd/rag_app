from typing import List
import pandas as pd
import arxiv
from app.schemas.data_fetcher import Article, FetchArxivArticleResponse
from app.utils.db import SessionLocal
from app.utils.cruds import article_crud
from  app.schemas.data_fetcher import ArticleInDB


async def fetch_articles_by_query(query:str="LLM",max_results:int=10,sort_criterion: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate ) -> FetchArxivArticleResponse:
  """search for articles in arxiv
  """
  articles : List[Article] = []

  client = arxiv.Client()

  search = arxiv.Search(
    query = query,
    max_results = max_results,
    sort_by =  arxiv.SortCriterion.Relevance 
  )

  for r in client.results(search):
    article = Article(title=r.title, summary=r.summary, pdf_url=r.pdf_url,published=pd.to_datetime(r.published))
    articles.append(article)
  
  result: FetchArxivArticleResponse = FetchArxivArticleResponse(fetched_articles=articles)

  return result

async def store_articles_into_db(articles: list[Article]) -> None:
  # Store articles in PostgreSQL database using CRUD operations
    db = SessionLocal()
    try:
        # Convert pydantic models to dict for bulk creation
        articles_data = [
            {
                "title": article.title,
                "summary": article.summary,
                "pdf_url": article.pdf_url,
                "published": article.published,
                "llm_summary": article.llm_summary
            }
            for article in articles
        ]
        
        # Use bulk create with duplicate checking
        stored_articles = article_crud.bulk_create_articles(db, articles_data)
        print(f"Successfully stored {len(stored_articles)} new articles in database")
        
    except Exception as e:
        print(f"Error storing articles in database: {e}")
    finally:
        db.close()
        
async def get_articles_from_db()-> list[ArticleInDB]:
  db = SessionLocal()
  try:
      articles = article_crud.get_articles(db=db, limit=200)    
      result = [ArticleInDB.model_validate(a) for a in articles] 
           
      print("Successfully getting articles from database")
      return result
      
  except Exception as e:
      print(f"Error getting articles from database: {e}")
      return []
  finally:
      db.close()