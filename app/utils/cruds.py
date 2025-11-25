from sqlalchemy.orm import  Session
from typing import List, Optional
from uuid import UUID
from app.models.data_fetcher import Article

# CRUD Operations

class ArticleCRUD:
    """CRUD operations for Article model"""
    
    @staticmethod
    def create_article(db: Session, article_data: dict) -> 'Article':
        """Create a new article"""
        from app.models.data_fetcher import Article
        
        db_article = Article(**article_data)
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article
    
    @staticmethod
    def get_article_by_id(db: Session, article_id: UUID) -> Optional['Article']:
        """Get article by ID"""
        from app.models.data_fetcher import Article
        
        return db.query(Article).filter(Article.id == article_id).first()
    
    @staticmethod
    def get_article_by_title(db: Session, title: str) -> Optional['Article']:
        """Get article by title"""
        from app.models.data_fetcher import Article
        
        return db.query(Article).filter(Article.title == title).first()
    
    @staticmethod
    def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List['Article']:
        """Get multiple articles with pagination"""
        from app.models.data_fetcher import Article
        
        return db.query(Article).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_article(db: Session, article_id: UUID, article_data: dict) -> Optional['Article']:
        """Update an existing article"""
        from app.models.data_fetcher import Article
        
        db_article = db.query(Article).filter(Article.id == article_id).first()
        if db_article:
            for key, value in article_data.items():
                setattr(db_article, key, value)
            db.commit()
            db.refresh(db_article)
        return db_article
    
    @staticmethod
    def delete_article(db: Session, article_id: UUID) -> bool:
        """Delete an article"""
        from app.models.data_fetcher import Article
        
        db_article = db.query(Article).filter(Article.id == article_id).first()
        if db_article:
            db.delete(db_article)
            db.commit()
            return True
        return False
    
    @staticmethod
    def bulk_create_articles(db: Session, articles_data: List[dict]) -> List['Article']:
        """Create multiple articles at once"""
        from app.models.data_fetcher import Article
        
        db_articles = []
        try:
            for article_data in articles_data:
                # Check if article already exists by title
                existing = db.query(Article).filter(Article.title == article_data.get('title')).first()
                if not existing:
                    db_article = Article(**article_data)
                    db.add(db_article)
                    db_articles.append(db_article)
            
            db.commit()
            for article in db_articles:
                db.refresh(article)
            return db_articles
        except Exception as e:
            db.rollback()
            raise e


# Create CRUD instance
article_crud = ArticleCRUD()