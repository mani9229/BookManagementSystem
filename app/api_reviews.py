# app/api_reviews.py
from typing import List
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, models
from app.database import get_db
from app.llm_utils import generate_review_summary
from app.api_auth import get_current_user #  Import get_current_user

review_router = APIRouter(prefix="/api/books/{book_id}/reviews", tags=["Reviews"])
@review_router.post("/", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = await crud.create_review(db, book_id, current_user.id, review, db)
    asyncio.create_task(generate_review_summary(book_id, db))
    return db_review
@review_router.get("/", response_model=List[schemas.ReviewResponse])
async def read_reviews_for_book(book_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                               db: AsyncSession = Depends(get_db),
                               current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    reviews = await crud.get_reviews_by_book(db, book_id, skip, limit)
    return reviews
@review_router.put("/{review_id}", response_model=schemas.ReviewResponse)
async def update_review(book_id: int, review_id: int, review: schemas.ReviewUpdate,
                         db: AsyncSession = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = await crud.get_review(db, review_id, book_id, db)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this review")
    return await crud.update_review(db, review_id, review, db)
@review_router.delete("/{review_id}", response_model=schemas.ReviewResponse)
async def delete_review(book_id: int, review_id: int, db: AsyncSession = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = await crud.get_review(db, review_id, book_id, db)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this review")
    return await crud.delete_review(db, review_id, db)
