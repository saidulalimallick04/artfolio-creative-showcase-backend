import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_me(client: AsyncClient, auth_headers):
    # auth_headers creates a user 'testuser_auth'
    response = await client.patch("/api/v1/users/me", data={
        "full_name": "Updated Name",
        "bio": "New Bio"
    }, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["bio"] == "New Bio"

@pytest.mark.asyncio
async def test_get_user_profile(client: AsyncClient):
    # Create a user to fetch
    await client.post("/api/v1/auth/register", json={
        "username": "profileuser",
        "email": "profile@example.com",
        "password": "password"
    })
    
    response = await client.get("/api/v1/users/profileuser")
    assert response.status_code == 200
    assert response.json()["username"] == "profileuser"

@pytest.mark.asyncio
async def test_deactivate_me(client: AsyncClient, auth_headers):
    response = await client.patch("/api/v1/users/me/deactivate", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify user is not in list (since list filters active=True)
    # We might need to ensure the user we deactivated is the one from auth_headers
    # auth_headers creates 'testuser_auth'
    
    response = await client.get("/api/v1/users/")
    users = response.json()
    usernames = [u["username"] for u in users]
    assert "testuser_auth" not in usernames
