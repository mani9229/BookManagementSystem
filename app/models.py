# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
import logging

logger = logging.getLogger(__name__)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    review_summary = Column(Text, nullable=True) # Adding review summary

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}')>"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Foreign Key to users table
    review_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews") # Relationship with User

    def __repr__(self):
        return f"<Review(review_text='{self.review_text}', rating='{self.rating}')>"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username='{self.username}')>"
