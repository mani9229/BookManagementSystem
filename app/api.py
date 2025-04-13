# app/api.py
from fastapi import APIRouter
from app.api_auth import auth_router
from app.api_books import book_router
from app.api_reviews import review_router
router = APIRouter()
router.include_router(auth_router)
router.include_router(book_router)
router.include_router(review_router)
