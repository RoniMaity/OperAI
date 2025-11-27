"""
Tests for authentication endpoints
"""

import pytest
from .conftest import auth_headers


@pytest.mark.asyncio
async def test_register_user(client):
    """Test user registration"""
    register_data = {
        "email": "newuser@test.com",
        "name": "New User",
        "password": "password123",
        "role": "employee"
    }
    
    response = await client.post("/api/auth/register", json=register_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["name"] == "New User"
    assert data["role"] == "employee"
    assert "id" in data
    assert "password" not in data  # Password should not be returned


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """Test that duplicate email registration fails"""
    register_data = {
        "email": "duplicate@test.com",
        "name": "User One",
        "password": "password123",
        "role": "employee"
    }
    
    # First registration should succeed
    response = await client.post("/api/auth/register", json=register_data)
    assert response.status_code == 200
    
    # Second registration with same email should fail
    register_data["name"] = "User Two"
    response = await client.post("/api/auth/register", json=register_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client):
    """Test successful login"""
    # Register user
    register_data = {
        "email": "logintest@test.com",
        "name": "Login Test",
        "password": "password123",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "logintest@test.com",
        "password": "password123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "logintest@test.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    # Register user
    register_data = {
        "email": "validuser@test.com",
        "name": "Valid User",
        "password": "correctpassword",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Try login with wrong password
    login_data = {
        "email": "validuser@test.com",
        "password": "wrongpassword"
    }
    response = await client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    login_data = {
        "email": "nonexistent@test.com",
        "password": "password123"
    }
    response = await client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_me_endpoint(client, employee_token):
    """Test /auth/me endpoint returns correct user data"""
    headers = auth_headers(employee_token["token"])
    response = await client.get("/api/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "employee@test.com"
    assert data["name"] == "Test Employee"
    assert data["role"] == "employee"
    assert data["id"] == employee_token["user_id"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_auth_me_without_token(client):
    """Test /auth/me endpoint without authentication"""
    response = await client.get("/api/auth/me")
    
    assert response.status_code == 403  # HTTPBearer returns 403 without token


@pytest.mark.asyncio
async def test_auth_me_invalid_token(client):
    """Test /auth/me endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = await client.get("/api/auth/me", headers=headers)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_all_roles(client):
    """Test registration for all roles"""
    roles = ["admin", "hr", "team_lead", "employee", "intern"]
    
    for role in roles:
        register_data = {
            "email": f"{role}@test.com",
            "name": f"Test {role}",
            "password": "password123",
            "role": role
        }
        
        response = await client.post("/api/auth/register", json=register_data)
        assert response.status_code == 200
        assert response.json()["role"] == role
