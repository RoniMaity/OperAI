"""
Basic smoke tests to verify critical API functionality
These tests run reliably and demonstrate test infrastructure
"""

import pytest
from .conftest import auth_headers


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint is accessible"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "OperAI" in data["message"]


@pytest.mark.asyncio
async def test_user_can_register(client):
    """Test basic user registration"""
    register_data = {
        "email": "smoke@test.com",
        "name": "Smoke Test User",
        "password": "password123",
        "role": "employee"
    }
    
    response = await client.post("/api/auth/register", json=register_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "smoke@test.com"
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_user_can_login_and_access_protected_route(client):
    """Test complete auth flow: register -> login -> access protected endpoint"""
    # Register
    register_data = {
        "email": "authflow@test.com",
        "name": "Auth Flow User",
        "password": "securepass",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "authflow@test.com",
        "password": "securepass"
    }
    login_response = await client.post("/api/auth/login", json=login_data)
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Access protected route
    headers = {"Authorization": f"Bearer {token}"}
    me_response = await client.get("/api/auth/me", headers=headers)
    
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "authflow@test.com"


@pytest.mark.asyncio
async def test_unauthorized_access_is_blocked(client):
    """Test that protected routes reject unauthorized access"""
    # Try to access without token
    response = await client.get("/api/auth/me")
    assert response.status_code == 403
    
    # Try with invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_employee_cannot_create_task(client):
    """Test RBAC - employee should not be able to create tasks"""
    # Register and login employee
    register_data = {
        "email": "rbac@test.com",
        "name": "RBAC Test",
        "password": "password",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    
    login_response = await client.post("/api/auth/login", json={
        "email": "rbac@test.com",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    
    # Try to create task
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {
        "title": "Should Fail",
        "assigned_to": login_response.json()["user"]["id"],
        "priority": "low"
    }
    
    response = await client.post("/api/tasks", json=task_data, headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_attendance_check_in_once_per_day(client):
    """Test attendance check-in is limited to once per day"""
    # Register and login
    register_data = {
        "email": "attendance@test.com",
        "name": "Attendance Test",
        "password": "password",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    
    login_response = await client.post("/api/auth/login", json={
        "email": "attendance@test.com",
        "password": "password"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # First check-in should succeed
    check_in_data = {"work_mode": "wfo"}
    response = await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    assert response.status_code == 200
    
    # Second check-in should fail
    response = await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    assert response.status_code == 400
    assert "already checked in" in response.json()["detail"].lower()
