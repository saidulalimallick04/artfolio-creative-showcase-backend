import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert "password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    # First registration
    await client.post("/api/v1/auth/register", json={
        "username": "user1",
        "email": "dup@example.com",
        "password": "password"
    })
    # Duplicate registration
    response = await client.post("/api/v1/auth/register", json={
        "username": "user2",
        "email": "dup@example.com", # Same email
        "password": "password"
    })
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Register
    await client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password"
    })
    # Login
    response = await client.post("/api/v1/auth/login", data={
        "username": "login@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login_failure(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
