from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func
from typing import List, Optional

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: schemas.BookCreate) -> Optional[models.Book]:
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in book_update.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def create_book_review(db: Session, book_id: int, review: schemas.ReviewCreate) -> models.Review:
    db_review = models.Review(book_id=book_id, **review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_book_reviews(db: Session, book_id: int) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()

def get_book_summary_and_rating(db: Session, book_id: int) -> Optional[dict]:
    book = get_book(db, book_id)
    if not book:
        return None

    average_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.book_id == book_id).scalar()

    return {"summary": book.summary, "average_rating": average_rating}
