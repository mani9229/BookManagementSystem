from pydantic import BaseModel, Field
from typing import List, Optional

class BookCreate(BaseModel):
    title: str = Field(..., max_length=255)
    author: str = Field(..., max_length=255)
    genre: str = Field(..., max_length=100)
    year_published: int
    summary: Optional[str] = None

class Book(BookCreate):
    id: int

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    user_id: int
    review_text: str
    rating: float = Field(..., ge=1, le=5)

class Review(ReviewCreate):
    id: int
    book_id: int

    class Config:
        orm_mode = True

class BookWithReviews(Book):
    reviews: List[Review] = []

class SummaryResponse(BaseModel):
    summary: str
    average_rating: Optional[float]
