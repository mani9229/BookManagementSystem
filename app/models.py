# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str = Field(None max_length=255)
    author: str = Field(None, max_length=255)
    genre: str = Field(None, max_length=100)
    year_published: int = Field(None, ge=1000, le=2025)
    content: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = Field(None, max_length=255)
    author: Optional[str] = Field(None, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    year_published: Optional[int] = Field(None, ge=1000, le=2025)
    content: Optional[str] = None

class BookResponse(BookBase):
    id: int
    summary: Optional[str] = None
    review_summary: Optional[str] = None

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    review_text: str
    rating: int = Field(None, ge=1, le=5)

class ReviewCreate(ReviewBase):
    user_id: int # Ensure user_id is part of creation

class ReviewUpdate(ReviewBase):
    review_text: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str = Field(None, max_length=50)

class UserCreate(UserBase):
    password: str = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    user_id: int

class RecommendationResponse(BaseModel):
    book_id: int
    title: str
    similarity_score: float
