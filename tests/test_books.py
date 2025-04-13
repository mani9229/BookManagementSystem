# tests/test_books.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
import json

async def test_create_book(async_client: AsyncClient, db: AsyncSession, test_user: models.User):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    book_data = {"title": "New Book", "author": "New Author", "genre": "Mystery", "year_published": 2024, "content": "New Content"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.post("/api/books/", json=book_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "New Book"

async def test_read_books(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get("/api/books/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

async def test_read_book(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get(f"/api/books/{test_book.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == test_book.title

async def test_update_book(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    updated_data = {"title": "Updated Book Title"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.put(f"/api/books/{test_book.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book Title"

async def test_delete_book(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.delete(f"/api/books/{test_book.id}", headers=headers)
    assert response.status_code == 200
    response = await async_client.get(f"/api/books/{test_book.id}", headers=headers)
    assert response.status_code == 404

async def test_get_book_summary(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get(f"/api/books/{test_book.id}/summary", headers=headers)
    assert response.status_code == 200
    #  We can't assert the exact summary, but we can check for a message or that the summary is eventually populated

async def test_get_book_recommendations(async_client: AsyncClient, db: AsyncSession, test_user: models.User, test_book: models.Book):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get(f"/api/books/{test_book.id}/recommendations/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
