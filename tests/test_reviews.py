# tests/test_reviews.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
import json

async def test_create_review(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    review_data = {"review_text": "Excellent book!", "rating": 5}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.post(f"/api/books/{test_book.id}/reviews/", json=review_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["review_text"] == "Excellent book!"

async def test_read_reviews_for_book(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book, test_review: models.Review):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get(f"/api/books/{test_book.id}/reviews/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

async def test_update_review(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book, test_review: models.Review):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    updated_data = {"review_text": "Updated review text", "rating": 4}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.put(f"/api/books/{test_book.id}/reviews/{test_review.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["review_text"] == "Updated review text"
    assert response.json()["rating"] == 4

async def test_delete_review(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book
