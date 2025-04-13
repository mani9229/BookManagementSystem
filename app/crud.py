# app/crud.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app import models, schemas
import logging

logger = logging.getLogger(__name__)

async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Book]:
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int) -> Optional[models.Book]:
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalars().first()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate) -> Optional[models.Book]:
    query = update(models.Book).where(models.Book.id == book_id).values(**book.dict(exclude_unset=True)).returning(models.Book)
    result = await db.execute(query)
    await db.commit()
    return result.scalars().first()

async def delete_book(db: AsyncSession, book_id: int) -> Optional[models.Book]:
    query = delete(models.Book).where(models.Book.id == book_id).returning(models.Book)
    result = await db.execute(query)
    await db.commit()
    return result.scalars().first()

async def create_review(db: AsyncSession, book_id: int, user_id: int, review: schemas.ReviewCreate) -> models.Review:
    db_review = models.Review(book_id=book_id, user_id=user_id, **review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_reviews_by_book(db: AsyncSession, book_id: int, skip: int = 0, limit: int = 100) -> List[models.Review]:
    result = await db.execute(select(models.Review).filter(models.Review.book_id == book_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_review(db: AsyncSession, review_id: int, book_id: int) -> Optional[models.Review]:
    result = await db.execute(select(models.Review).filter(models.Review.id == review_id, models.Review.book_id == book_id))
    return result.scalars().first()

async def update_review(db: AsyncSession, review_id: int, review: schemas.ReviewUpdate) -> Optional[models.Review]:
    query = update(models.Review).where(models.Review.id == review_id).values(**review.dict(exclude_unset=True)).returning(models.Review)
    result = await db.execute(query)
    await db.commit()
    return result.scalars().first()

async def delete_review(db: AsyncSession, review_id: int, db: AsyncSession) -> Optional[models.Review]:
    query = delete(models.Review).where(models.Review.id == review_id).returning(models.Review)
    result = await db.execute(query)
    await db.commit()
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]: #  For auth
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()
