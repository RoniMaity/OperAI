"""
Tests for leave management endpoints
"""

import pytest
from datetime import datetime, timezone, timedelta
from .conftest import auth_headers


@pytest.mark.asyncio
async def test_employee_can_apply_leave(client, employee_token):
    """Test employee can apply for leave"""
    headers = auth_headers(employee_token["token"])
    
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "casual",
        "start_date": (today + timedelta(days=7)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=9)).strftime('%Y-%m-%d'),
        "reason": "Family vacation"
    }
    
    response = await client.post("/api/leave", json=leave_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == employee_token["user_id"]
    assert data["leave_type"] == "casual"
    assert data["start_date"] == leave_data["start_date"]
    assert data["end_date"] == leave_data["end_date"]
    assert data["reason"] == "Family vacation"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_employee_can_view_own_leaves(client, employee_token):
    """Test employee can view their own leave applications"""
    headers = auth_headers(employee_token["token"])
    
    # Apply for leave
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "sick",
        "start_date": (today + timedelta(days=1)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=2)).strftime('%Y-%m-%d'),
        "reason": "Medical checkup"
    }
    await client.post("/api/leave", json=leave_data, headers=headers)
    
    # Get leave list
    response = await client.get("/api/leave", headers=headers)
    
    assert response.status_code == 200
    leaves = response.json()
    assert len(leaves) == 1
    assert leaves[0]["user_id"] == employee_token["user_id"]
    assert leaves[0]["leave_type"] == "sick"


@pytest.mark.asyncio
async def test_hr_can_view_all_leaves(client, hr_token, employee_token):
    """Test HR can view all leave applications"""
    # Employee applies for leave
    emp_headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "earned",
        "start_date": (today + timedelta(days=10)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=14)).strftime('%Y-%m-%d'),
        "reason": "Annual leave"
    }
    await client.post("/api/leave", json=leave_data, headers=emp_headers)
    
    # HR views all leaves
    hr_headers = auth_headers(hr_token)
    response = await client.get("/api/leave", headers=hr_headers)
    
    assert response.status_code == 200
    leaves = response.json()
    assert len(leaves) >= 1


@pytest.mark.asyncio
async def test_hr_can_approve_leave(client, hr_token, employee_token):
    """Test HR can approve leave application"""
    # Employee applies for leave
    emp_headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "casual",
        "start_date": (today + timedelta(days=5)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=6)).strftime('%Y-%m-%d'),
        "reason": "Personal work"
    }
    create_response = await client.post("/api/leave", json=leave_data, headers=emp_headers)
    leave_id = create_response.json()["id"]
    
    # HR approves leave
    hr_headers = auth_headers(hr_token)
    update_data = {
        "status": "approved"
    }
    response = await client.patch(f"/api/leave/{leave_id}", json=update_data, headers=hr_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["approved_by"] is not None


@pytest.mark.asyncio
async def test_hr_can_reject_leave(client, hr_token, employee_token):
    """Test HR can reject leave application"""
    # Employee applies for leave
    emp_headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "unpaid",
        "start_date": (today + timedelta(days=3)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=5)).strftime('%Y-%m-%d'),
        "reason": "Extended vacation"
    }
    create_response = await client.post("/api/leave", json=leave_data, headers=emp_headers)
    leave_id = create_response.json()["id"]
    
    # HR rejects leave
    hr_headers = auth_headers(hr_token)
    update_data = {
        "status": "rejected",
        "rejection_reason": "Insufficient leave balance"
    }
    response = await client.patch(f"/api/leave/{leave_id}", json=update_data, headers=hr_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"
    assert data["rejection_reason"] == "Insufficient leave balance"


@pytest.mark.asyncio
async def test_team_lead_can_approve_leave(client, team_lead_token, employee_token):
    """Test team lead can also approve leave applications"""
    # Employee applies for leave
    emp_headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "sick",
        "start_date": (today + timedelta(days=1)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=1)).strftime('%Y-%m-%d'),
        "reason": "Flu"
    }
    create_response = await client.post("/api/leave", json=leave_data, headers=emp_headers)
    leave_id = create_response.json()["id"]
    
    # Team lead approves
    lead_headers = auth_headers(team_lead_token["token"])
    update_data = {"status": "approved"}
    response = await client.patch(f"/api/leave/{leave_id}", json=update_data, headers=lead_headers)
    
    assert response.status_code == 200
    assert response.json()["status"] == "approved"


@pytest.mark.asyncio
async def test_employee_cannot_approve_own_leave(client, employee_token):
    """Test employee cannot approve their own leave"""
    headers = auth_headers(employee_token["token"])
    
    # Apply for leave
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "casual",
        "start_date": (today + timedelta(days=2)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=3)).strftime('%Y-%m-%d'),
        "reason": "Personal"
    }
    create_response = await client.post("/api/leave", json=leave_data, headers=headers)
    leave_id = create_response.json()["id"]
    
    # Try to approve own leave
    update_data = {"status": "approved"}
    response = await client.patch(f"/api/leave/{leave_id}", json=update_data, headers=headers)
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_leave_types_are_valid(client, employee_token):
    """Test different leave types can be applied"""
    headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    
    leave_types = ["sick", "casual", "earned", "unpaid"]
    
    for leave_type in leave_types:
        leave_data = {
            "leave_type": leave_type,
            "start_date": (today + timedelta(days=5)).strftime('%Y-%m-%d'),
            "end_date": (today + timedelta(days=6)).strftime('%Y-%m-%d'),
            "reason": f"Testing {leave_type} leave"
        }
        response = await client.post("/api/leave", json=leave_data, headers=headers)
        
        assert response.status_code == 200
        assert response.json()["leave_type"] == leave_type


@pytest.mark.asyncio
async def test_hr_can_filter_leaves_by_status(client, hr_token, employee_token):
    """Test HR can filter leaves by status"""
    # Employee applies for multiple leaves
    emp_headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    
    # Create pending leave
    leave_data = {
        "leave_type": "casual",
        "start_date": (today + timedelta(days=10)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=11)).strftime('%Y-%m-%d'),
        "reason": "Pending leave"
    }
    await client.post("/api/leave", json=leave_data, headers=emp_headers)
    
    # HR filters by pending status
    hr_headers = auth_headers(hr_token)
    response = await client.get("/api/leave?status=pending", headers=hr_headers)
    
    assert response.status_code == 200
    leaves = response.json()
    assert len(leaves) >= 1
    for leave in leaves:
        assert leave["status"] == "pending"


@pytest.mark.asyncio
async def test_leave_status_update_modifies_updated_at(client, hr_token, employee_token):
    """Test that approving/rejecting leave updates the updated_at field"""
    # Employee applies
    emp_headers = auth_headers(employee_token["token"])
    today = datetime.now(timezone.utc)
    leave_data = {
        "leave_type": "sick",
        "start_date": (today + timedelta(days=1)).strftime('%Y-%m-%d'),
        "end_date": (today + timedelta(days=2)).strftime('%Y-%m-%d'),
        "reason": "Medical"
    }
    create_response = await client.post("/api/leave", json=leave_data, headers=emp_headers)
    leave = create_response.json()
    leave_id = leave["id"]
    created_at = leave["created_at"]
    
    # HR approves
    hr_headers = auth_headers(hr_token)
    update_data = {"status": "approved"}
    response = await client.patch(f"/api/leave/{leave_id}", json=update_data, headers=hr_headers)
    
    assert response.status_code == 200
    updated_leave = response.json()
    assert updated_leave["updated_at"] != created_at  # Should be different
    assert updated_leave["status"] == "approved"
