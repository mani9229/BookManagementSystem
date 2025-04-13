# app/api_books.py
from typing import List, Optional
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas, crud, models
from app.database import get_db
from app.llm_utils import generate_book_summary
from app.api_auth import get_current_user #  Import get_current_user

book_router = APIRouter(prefix="/api/books", tags=["Books"])
@book_router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    db_book = await crud.create_book(db, book)
    asyncio.create_task(generate_book_summary(db_book.id, db))
    return db_book
@book_router.get("/", response_model=List[schemas.BookResponse])
async def read_books(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
                     db: AsyncSession = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)):
    books = await crud.get_books(db, skip, limit)
    return books
@book_router.get("/{book_id}", response_model=schemas.BookResponse)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
@book_router.put("/{book_id}", response_model=schemas.BookResponse)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await crud.update_book(db, book_id, book)
@book_router.delete("/{book_id}", response_model=schemas.BookResponse)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await crud.delete_book(db, book_id)
@book_router.get("/{book_id}/summary", response_model=schemas.BookResponse)
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_db),
                           current_user: models.User = Depends(get_current_user)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not db_book.summary:
        asyncio.create_task(generate_book_summary(book_id, db))
        return {"message": "Summary generation started. Please check back later."}
    return db_book
@book_router.get("/{book_id}/recommendations/", response_model=List[schemas.RecommendationResponse])
async def get_book_recommendations(book_id: int, db: AsyncSession = Depends(get_db),
                                   current_user: models.User = Depends(get_current_user)):
    target_book = await crud.get_book(db, book_id)
    if not target_book:
        raise HTTPException(status_code=404, detail="Book not found")
    all_books = await crud.get_books(db, skip=0, limit=1000)
    if not all_books:
        return []
    # Basic Recommendation (Replace with better logic)
    import random
    if len(all_books) <= 5:
        return [{"book_id": book.id, "title": book.title, "similarity_score": 1.0} for book in all_books]
    else:
        recommended_books = random.sample(all_books, 5)
        return [{"book_id": book.id, "title": book.title, "similarity_score": 0.8} for book in recommended_books]
