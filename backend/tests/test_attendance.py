"""
Tests for attendance endpoints
"""

import pytest
from datetime import datetime, timezone
from .conftest import auth_headers


@pytest.mark.asyncio
async def test_employee_can_check_in(client, employee_token):
    """Test employee can check-in for attendance"""
    headers = auth_headers(employee_token["token"])
    
    check_in_data = {
        "work_mode": "wfo"
    }
    
    response = await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == employee_token["user_id"]
    assert data["date"] == datetime.now(timezone.utc).strftime('%Y-%m-%d')
    assert data["status"] == "present"
    assert data["work_mode"] == "wfo"
    assert data["check_in"] is not None
    assert data["check_out"] is None


@pytest.mark.asyncio
async def test_employee_can_check_in_wfh(client, employee_token):
    """Test employee can check-in with WFH mode"""
    headers = auth_headers(employee_token["token"])
    
    check_in_data = {
        "work_mode": "wfh"
    }
    
    response = await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "wfh"
    assert data["work_mode"] == "wfh"


@pytest.mark.asyncio
async def test_cannot_check_in_twice_same_day(client, employee_token):
    """Test that employee cannot check-in twice on the same day"""
    headers = auth_headers(employee_token["token"])
    
    # First check-in
    check_in_data = {"work_mode": "wfo"}
    response = await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    assert response.status_code == 200
    
    # Second check-in attempt
    response = await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    
    assert response.status_code == 400
    assert "already checked in" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_employee_can_check_out(client, employee_token):
    """Test employee can check-out after check-in"""
    headers = auth_headers(employee_token["token"])
    
    # Check-in first
    check_in_data = {"work_mode": "wfo"}
    await client.post("/api/attendance/check-in", json=check_in_data, headers=headers)
    
    # Check-out
    check_out_data = {
        "notes": "Completed all tasks for today"
    }
    response = await client.post("/api/attendance/check-out", json=check_out_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["check_in"] is not None
    assert data["check_out"] is not None
    assert data["notes"] == "Completed all tasks for today"


@pytest.mark.asyncio
async def test_cannot_check_out_without_check_in(client, employee_token):
    """Test that employee cannot check-out without checking-in first"""
    headers = auth_headers(employee_token["token"])
    
    check_out_data = {"notes": "Trying to check out"}
    response = await client.post("/api/attendance/check-out", json=check_out_data, headers=headers)
    
    assert response.status_code == 400
    assert "not checked in" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_cannot_check_out_twice(client, employee_token):
    """Test that employee cannot check-out twice"""
    headers = auth_headers(employee_token["token"])
    
    # Check-in
    await client.post("/api/attendance/check-in", json={"work_mode": "wfo"}, headers=headers)
    
    # First check-out
    response = await client.post("/api/attendance/check-out", json={}, headers=headers)
    assert response.status_code == 200
    
    # Second check-out attempt
    response = await client.post("/api/attendance/check-out", json={}, headers=headers)
    
    assert response.status_code == 400
    assert "already checked out" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_employee_can_view_own_attendance(client, employee_token):
    """Test employee can view their attendance records"""
    headers = auth_headers(employee_token["token"])
    
    # Check-in
    await client.post("/api/attendance/check-in", json={"work_mode": "wfh"}, headers=headers)
    
    # Get attendance records
    response = await client.get("/api/attendance", headers=headers)
    
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["user_id"] == employee_token["user_id"]
    assert records[0]["work_mode"] == "wfh"


@pytest.mark.asyncio
async def test_hr_can_view_all_attendance(client, hr_token, employee_token):
    """Test HR can view attendance records of all employees"""
    # Employee checks in
    emp_headers = auth_headers(employee_token["token"])
    await client.post("/api/attendance/check-in", json={"work_mode": "wfo"}, headers=emp_headers)
    
    # HR views all attendance
    hr_headers = auth_headers(hr_token)
    response = await client.get("/api/attendance", headers=hr_headers)
    
    assert response.status_code == 200
    records = response.json()
    assert len(records) >= 1  # Should see at least the employee's attendance


@pytest.mark.asyncio
async def test_hr_can_filter_attendance_by_user(client, hr_token, employee_token):
    """Test HR can filter attendance by specific user"""
    # Employee checks in
    emp_headers = auth_headers(employee_token["token"])
    await client.post("/api/attendance/check-in", json={"work_mode": "wfo"}, headers=emp_headers)
    
    # HR filters by user
    hr_headers = auth_headers(hr_token)
    response = await client.get(
        f"/api/attendance?user_id={employee_token['user_id']}", 
        headers=hr_headers
    )
    
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["user_id"] == employee_token["user_id"]


@pytest.mark.asyncio
async def test_attendance_date_is_correct(client, employee_token):
    """Test that attendance date is set to current date"""
    headers = auth_headers(employee_token["token"])
    
    response = await client.post("/api/attendance/check-in", 
                                 json={"work_mode": "wfo"}, 
                                 headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    assert data["date"] == today


@pytest.mark.asyncio
async def test_multiple_employees_can_check_in_same_day(client):
    """Test that multiple employees can check-in on the same day"""
    # Create and login two employees
    employees = []
    for i in range(2):
        register_data = {
            "email": f"emp{i}@test.com",
            "name": f"Employee {i}",
            "password": "password123",
            "role": "employee"
        }
        await client.post("/api/auth/register", json=register_data)
        
        login_response = await client.post("/api/auth/login", json={
            "email": f"emp{i}@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        employees.append(token)
    
    # Both employees check-in
    for token in employees:
        headers = auth_headers(token)
        response = await client.post("/api/attendance/check-in", 
                                     json={"work_mode": "wfo"}, 
                                     headers=headers)
        assert response.status_code == 200
