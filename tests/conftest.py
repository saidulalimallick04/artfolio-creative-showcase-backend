import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from main import app
from core.config import settings
from models.user import User
from models.artwork import Artwork

# Override settings for testing
settings.MONGODB_URL = "mongodb://localhost:27017/artfolio_test"

@pytest_asyncio.fixture(scope="function")
async def db_client():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client.artfolio_test, document_models=[User, Artwork])
    yield client
    # Cleanup after tests
    await client.drop_database("artfolio_test")
    client.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_client) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture(scope="function")
async def auth_headers(client: AsyncClient):
    # Register and Login a test user to get token
    user_data = {
        "username": "testuser_auth",
        "email": "auth@example.com",
        "password": "password123"
    }
    await client.post("/api/v1/auth/register", json=user_data)
    
    response = await client.post("/api/v1/auth/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
