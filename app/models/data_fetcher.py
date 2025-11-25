from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.utils.db import Base

class Article(Base):
    __tablename__ = "Article"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    llm_summary = Column(String, nullable=True)
    pdf_url = Column(String)
    published = Column(DateTime, default=False)
