import pytest
from .conftest import auth_headers

@pytest.mark.asyncio
async def test_employee_cannot_update_progress(client, team_lead_token, employee_token):
    """Test that employee cannot update progress of their assigned task"""
    # Team lead creates task
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Progress Restriction Task",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    # Employee tries to update progress
    emp_headers = auth_headers(employee_token["token"])
    update_data = {
        "progress": 50
    }
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=emp_headers)
    
    # This should fail after the fix, but currently it passes (200)
    # I will assert 200 first to confirm current behavior, then change to 403 after fix
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_employee_can_update_status_without_progress(client, team_lead_token, employee_token):
    """Test that employee can still update status"""
    # Team lead creates task
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Status Update Task",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    # Employee updates status only
    emp_headers = auth_headers(employee_token["token"])
    update_data = {
        "status": "in_progress"
    }
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=emp_headers)
    
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_creator_can_update_progress(client, team_lead_token, employee_token):
    """Test that task creator (Team Lead) can update progress"""
    # Team lead creates task
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Creator Update Task",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    # Team lead updates progress
    update_data = {
        "progress": 75
    }
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=lead_headers)
    
    assert response.status_code == 200
    assert response.json()["progress"] == 75
