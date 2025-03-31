from app.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(db.Text, nullable=True)  # Can be nullable

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  # Simple user ID for now
    review_text = Column(db.Text, nullable=False)
    rating = Column(Float, nullable=False)

    book = relationship("Book", back_populates="reviews")
