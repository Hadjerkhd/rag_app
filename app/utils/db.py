from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

url = URL.create(
    drivername="postgresql",
    username=settings.PG_DB_USER_NAME,
    host=settings.PG_DB_HOST,
    port=settings.PG_DB_PORT,
    database=settings.PG_DB_NAME,
    password=settings.PG_password
)

engine = create_engine(url)

# Create declarative base for models
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency
def get_db() -> Session: #type: ignore
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
