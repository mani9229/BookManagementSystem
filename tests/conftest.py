# tests/conftest.py
# pytest configuration (e.g., fixtures)
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool # Important for testing
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app import models
from typing import AsyncGenerator

# Override the database URL for testing (in-memory SQLite)
TEST_DATABASE_URL = "postgresql://neondb_owner:npg_d9JMeauYP4Oj@ep-damp-unit-a59836nl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"       ##This is connection string for my DB ,which can be used as a test db

# Create a new async engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool) # No pooling for tests
TestAsyncSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

# Override get_db dependency
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

# Create and drop tables for each test session
@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Async client fixture
@pytest.fixture(name="async_client")
async def get_async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Test data fixtures (example)
@pytest.fixture
async def test_user(db: AsyncSession) -> models.User:
    user_data = {"username": "testuser", "password": "testpassword"}
    user = models.User(username=user_data["username"], hashed_password="hashed_password") # Hash in tests if needed
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@pytest.fixture
async def test_book(db: AsyncSession) -> models.Book:
    book_data = {"title": "Test Book", "author": "Test Author", "genre": "Fiction", "year_published": 2024, "content": "Test Content"}
    book = models.Book(**book_data)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

@pytest.fixture
async def test_review(db: AsyncSession, test_book: models.Book, test_user: models.User) -> models.Review:
    review_data = {"review_text": "Great book!", "rating": 5}
    review = models.Review(book_id=test_book.id, user_id=test_user.id, **review_data)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

# Database session fixture
@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session
