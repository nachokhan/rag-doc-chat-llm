import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    pages = relationship("Page", back_populates="document", cascade="all, delete-orphan")
    facts = relationship("Fact", back_populates="document", cascade="all, delete-orphan")

class Page(Base):
    __tablename__ = "pages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384)) # openai embedding dimension

    document = relationship("Document", back_populates="pages")

class Fact(Base):
    __tablename__ = "facts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    label = Column(String, nullable=False)
    value_text = Column(String, nullable=False)
    page = Column(Integer, nullable=False)
    embedding = Column(Vector(384)) # openai embedding dimension

    document = relationship("Document", back_populates="facts")
