# app/llm_utils.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from llama_cpp import Llama
from app.config import settings
from app import models
import logging

logger = logging.getLogger(__name__)

LLM = Llama(model_path=settings.LLAMA_MODEL_PATH)

async def generate_book_summary(book_id: int, db: AsyncSession):
    try:
        book = await db.execute(select(models.Book).filter(models.Book.id == book_id))
        book = book.scalars().first()
        if not book:
            logger.warning(f"Book with ID {book_id} not found.")
            return

        prompt = f"Summarize the following book content: {book.content}"
        output = LLM(prompt, max_tokens=256, echo=False)
        summary = output["choices"][0]["text"]

        book.summary = summary
        await db.commit()
    except Exception as e:
        logger.error(f"Error generating summary for book {book_id}: {e}")
        await db.rollback()

async def generate_review_summary(book_id: int, db: AsyncSession):
    try:
        reviews = await db.execute(select(models.Review).filter(models.Review.book_id == book_id))
        reviews = reviews.scalars().all()
        if not reviews:
            logger.info(f"No reviews available for book {book_id}.")
            return

        review_texts = [review.review_text for review in reviews]
        prompt = f"Summarize the following reviews: {review_texts}"
        output = LLM(prompt, max_tokens=128, echo=False)
        summary = output["choices"][0]["text"]

        book = await db.execute(select(models.Book).filter(models.Book.id == book_id))
        book = book.scalars().first()
        if book:
            book.review_summary = summary
            await db.commit()
        else:
            logger.warning(f"Book with ID {book_id} not found.")
    except Exception as e:
        logger.error(f"Error generating review summary for book {book_id}: {e}")
        await db.rollback()
