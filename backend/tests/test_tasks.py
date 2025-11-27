"""
Tests for task management endpoints
"""

import pytest
from datetime import datetime, timezone, timedelta
from .conftest import auth_headers


@pytest.mark.asyncio
async def test_team_lead_can_create_task(client, team_lead_token, employee_token):
    """Test that team lead can create tasks"""
    headers = auth_headers(team_lead_token["token"])
    
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "assigned_to": employee_token["user_id"],
        "priority": "high",
        "deadline": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    }
    
    response = await client.post("/api/tasks", json=task_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["assigned_to"] == employee_token["user_id"]
    assert data["created_by"] == team_lead_token["user_id"]
    assert data["status"] == "todo"
    assert data["priority"] == "high"
    assert data["progress"] == 0


@pytest.mark.asyncio
async def test_hr_can_create_task(client, hr_token, employee_token):
    """Test that HR can create tasks"""
    headers = auth_headers(hr_token)
    
    task_data = {
        "title": "HR Task",
        "description": "Task from HR",
        "assigned_to": employee_token["user_id"],
        "priority": "medium"
    }
    
    response = await client.post("/api/tasks", json=task_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["title"] == "HR Task"


@pytest.mark.asyncio
async def test_employee_cannot_create_task(client, employee_token):
    """Test that regular employee cannot create tasks"""
    headers = auth_headers(employee_token["token"])
    
    task_data = {
        "title": "Should Fail",
        "description": "Employee trying to create task",
        "assigned_to": employee_token["user_id"],
        "priority": "low"
    }
    
    response = await client.post("/api/tasks", json=task_data, headers=headers)
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_employee_can_list_own_tasks(client, team_lead_token, employee_token):
    """Test that employee can only see their own tasks"""
    # Team lead creates task for employee
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Employee Task",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    await client.post("/api/tasks", json=task_data, headers=lead_headers)
    
    # Employee lists tasks
    emp_headers = auth_headers(employee_token["token"])
    response = await client.get("/api/tasks", headers=emp_headers)
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["assigned_to"] == employee_token["user_id"]
    assert tasks[0]["title"] == "Employee Task"


@pytest.mark.asyncio
async def test_team_lead_sees_created_tasks(client, team_lead_token, employee_token):
    """Test that team lead can see tasks they created"""
    headers = auth_headers(team_lead_token["token"])
    
    # Create multiple tasks
    for i in range(3):
        task_data = {
            "title": f"Task {i+1}",
            "assigned_to": employee_token["user_id"],
            "priority": "medium"
        }
        await client.post("/api/tasks", json=task_data, headers=headers)
    
    # List tasks as team lead
    response = await client.get("/api/tasks", headers=headers)
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
    for task in tasks:
        assert task["created_by"] == team_lead_token["user_id"]


@pytest.mark.asyncio
async def test_employee_can_update_own_task_status(client, team_lead_token, employee_token):
    """Test that employee can update status of their assigned task"""
    # Team lead creates task
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Task to Update",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    # Employee updates task
    emp_headers = auth_headers(employee_token["token"])
    update_data = {
        "status": "in_progress",
        "progress": 50
    }
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=emp_headers)
    
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["status"] == "in_progress"
    assert updated_task["progress"] == 50


@pytest.mark.asyncio
async def test_employee_cannot_update_others_task(client, team_lead_token, employee_token):
    """Test that employee cannot update tasks not assigned to them"""
    # Create second employee
    register_data = {
        "email": "employee2@test.com",
        "name": "Employee Two",
        "password": "emp123",
        "role": "employee"
    }
    await client.post("/api/auth/register", json=register_data)
    login_response = await client.post("/api/auth/login", json={
        "email": "employee2@test.com",
        "password": "emp123"
    })
    employee2_id = login_response.json()["user"]["id"]
    
    # Team lead creates task for employee2
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Task for Employee 2",
        "assigned_to": employee2_id,
        "priority": "medium"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    # Employee 1 tries to update employee 2's task
    emp_headers = auth_headers(employee_token["token"])
    update_data = {"status": "completed"}
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=emp_headers)
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_task_progress_validation(client, team_lead_token, employee_token):
    """Test that task progress is clamped to 0-100"""
    # Create task
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Progress Test Task",
        "assigned_to": employee_token["user_id"],
        "priority": "low"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    # Try to set progress > 100
    emp_headers = auth_headers(employee_token["token"])
    update_data = {"progress": 150}
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=emp_headers)
    
    assert response.status_code == 200
    assert response.json()["progress"] == 100  # Should be clamped to 100
    
    # Try to set progress < 0
    update_data = {"progress": -10}
    response = await client.patch(f"/api/tasks/{task_id}", json=update_data, headers=emp_headers)
    
    assert response.status_code == 200
    assert response.json()["progress"] == 0  # Should be clamped to 0


@pytest.mark.asyncio
async def test_task_status_transitions(client, team_lead_token, employee_token):
    """Test task status can transition properly"""
    # Create task
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "Status Transition Task",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    create_response = await client.post("/api/tasks", json=task_data, headers=lead_headers)
    task_id = create_response.json()["id"]
    
    emp_headers = auth_headers(employee_token["token"])
    
    # todo -> in_progress
    response = await client.patch(f"/api/tasks/{task_id}", 
                                  json={"status": "in_progress"}, 
                                  headers=emp_headers)
    assert response.json()["status"] == "in_progress"
    
    # in_progress -> completed
    response = await client.patch(f"/api/tasks/{task_id}", 
                                  json={"status": "completed"}, 
                                  headers=emp_headers)
    assert response.json()["status"] == "completed"
    assert response.json()["progress"] == 100  # Auto-set to 100 when completed


@pytest.mark.asyncio
async def test_hr_can_view_all_tasks(client, hr_token, team_lead_token, employee_token):
    """Test that HR can view all tasks in the system"""
    # Team lead creates tasks
    lead_headers = auth_headers(team_lead_token["token"])
    for i in range(2):
        await client.post("/api/tasks", json={
            "title": f"Task {i+1}",
            "assigned_to": employee_token["user_id"],
            "priority": "medium"
        }, headers=lead_headers)
    
    # HR views all tasks
    hr_headers = auth_headers(hr_token)
    response = await client.get("/api/tasks", headers=hr_headers)
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2  # Should see at least the 2 tasks created
