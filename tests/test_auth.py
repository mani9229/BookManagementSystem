# tests/test_auth.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
import json

async def test_register_user(async_client: AsyncClient, db: AsyncSession):
    user_data = {"username": "newuser", "password": "newpassword"}
    response = await async_client.post("/auth/register/", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

    # Check if user is in the database
    user = await db.execute(select(models.User).filter(models.User.username == "newuser"))
    assert user.scalars().first() is not None

async def test_login_user(async_client: AsyncClient, test_user: models.User):
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    response = await async_client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_login_user_incorrect_password(async_client: AsyncClient, test_user: models.User):
    login_data = {"username": "testuser", "password": "wrongpassword"}
    response = await async_client.post("/auth/token", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

async def test_get_current_user(async_client: AsyncClient, test_user: models.User):
    # First, log in to get a token
    login_data = {"username": "testuser", "password": "testpassword"} #  Assuming 'testpassword' was the password
    login_response = await async_client.post("/auth/token", data=login_data)
    access_token = login_response.json()["access_token"]

    # Then, use the token to access a protected route
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get("/api/books/", headers=headers) #  Any protected route will do
    assert response.status_code == 200
