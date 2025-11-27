"""
Pytest configuration and fixtures for OperAI backend tests
"""

import pytest
import os
import asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Override DB name for tests
TEST_DB_NAME = "workforceos_test_db"
os.environ['DB_NAME'] = TEST_DB_NAME


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """
    Provide a clean test database for each test.
    Clears all collections before and after each test.
    """
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[TEST_DB_NAME]
    
    # Clear all collections before test
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].delete_many({})
    
    yield db
    
    # Clear all collections after test
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].delete_many({})
    
    client.close()


@pytest.fixture(scope="function")
async def client(test_db):
    """
    Provide an async HTTP client for testing FastAPI endpoints.
    """
    # Import server here to ensure test DB is set
    from server import app
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_token(client):
    """Create and login an admin user, return auth token"""
    # Register admin
    register_data = {
        "email": "admin@test.com",
        "name": "Test Admin",
        "password": "admin123",
        "role": "admin"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "admin@test.com",
        "password": "admin123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    return response.json()["access_token"]


@pytest.fixture
async def hr_token(client):
    """Create and login an HR user, return auth token"""
    # Register HR
    register_data = {
        "email": "hr@test.com",
        "name": "Test HR",
        "password": "hr123",
        "role": "hr"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "hr@test.com",
        "password": "hr123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    return response.json()["access_token"]


@pytest.fixture
async def team_lead_token(client):
    """Create and login a team lead user, return auth token and user data"""
    # Register team lead
    register_data = {
        "email": "lead@test.com",
        "name": "Test Lead",
        "password": "lead123",
        "role": "team_lead"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "lead@test.com",
        "password": "lead123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    data = response.json()
    return {
        "token": data["access_token"],
        "user_id": data["user"]["id"]
    }


@pytest.fixture
async def employee_token(client):
    """Create and login an employee user, return auth token and user data"""
    # Register employee
    register_data = {
        "email": "employee@test.com",
        "name": "Test Employee",
        "password": "emp123",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "employee@test.com",
        "password": "emp123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    data = response.json()
    return {
        "token": data["access_token"],
        "user_id": data["user"]["id"]
    }


@pytest.fixture
async def intern_token(client):
    """Create and login an intern user, return auth token"""
    # Register intern
    register_data = {
        "email": "intern@test.com",
        "name": "Test Intern",
        "password": "intern123",
        "role": "intern"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "intern@test.com",
        "password": "intern123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    return response.json()["access_token"]


def auth_headers(token: str) -> dict:
    """Helper to create authorization headers"""
    return {"Authorization": f"Bearer {token}"}
