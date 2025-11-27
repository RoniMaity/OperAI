"""
Tests for AI assistant endpoints with mocked LLM calls
"""

import pytest
from unittest.mock import AsyncMock, patch
from .conftest import auth_headers


@pytest.mark.asyncio
async def test_ai_chat_endpoint_returns_response(client, employee_token):
    """Test /api/ai/chat endpoint returns a response"""
    headers = auth_headers(employee_token["token"])
    
    # Mock the LlmChat
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        mock_instance.send_message = AsyncMock(return_value="Hello! I'm OperAI Intelligence. How can I help you today?")
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Hello",
            "session_id": "test-session-123"
        }
        
        response = await client.post("/api/ai/chat", json=ai_request, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert data["session_id"] == "test-session-123"


@pytest.mark.asyncio
async def test_ai_execute_endpoint_basic(client, employee_token):
    """Test /api/ai/execute endpoint with mocked LLM"""
    headers = auth_headers(employee_token["token"])
    
    # Mock the LlmChat to return valid JSON
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        # Simulate AI returning a valid action response
        mock_response = """{
            "thought": "User wants to see their tasks",
            "actions": [
                {
                    "name": "list_user_tasks",
                    "params": {}
                }
            ]
        }"""
        mock_instance.send_message = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Show me my tasks",
            "session_id": "test-session-456"
        }
        
        response = await client.post("/api/ai/execute", json=ai_request, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or "thought" in data
        assert "actionsExecuted" in data
        assert isinstance(data["actionsExecuted"], list)


@pytest.mark.asyncio
async def test_ai_execute_returns_structured_json(client, employee_token):
    """Test that /api/ai/execute returns properly structured JSON"""
    headers = auth_headers(employee_token["token"])
    
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        mock_response = """{
            "thought": "Executing task list action",
            "actions": [
                {
                    "name": "summarize_tasks",
                    "params": {}
                }
            ]
        }"""
        mock_instance.send_message = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Summarize my tasks",
            "session_id": "test-session-789"
        }
        
        response = await client.post("/api/ai/execute", json=ai_request, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "session_id" in data
        assert "actionsExecuted" in data
        assert data["session_id"] == "test-session-789"
        
        # Verify actions executed is a list
        assert isinstance(data["actionsExecuted"], list)


@pytest.mark.asyncio
async def test_ai_execute_with_malformed_json(client, employee_token):
    """Test /api/ai/execute handles malformed JSON gracefully"""
    headers = auth_headers(employee_token["token"])
    
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        # Return malformed JSON
        mock_response = "This is not valid JSON at all!"
        mock_instance.send_message = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Test malformed response",
            "session_id": "test-session-error"
        }
        
        response = await client.post("/api/ai/execute", json=ai_request, headers=headers)
        
        # Should still return 200 but with error handled gracefully
        assert response.status_code == 200
        data = response.json()
        assert "actionsExecuted" in data
        assert data["actionsExecuted"] == []  # No actions executed due to parse error


@pytest.mark.asyncio
async def test_ai_execute_action_execution(client, team_lead_token, employee_token):
    """Test that AI can execute actions like listing tasks"""
    # Team lead creates a task for employee
    lead_headers = auth_headers(team_lead_token["token"])
    task_data = {
        "title": "AI Test Task",
        "assigned_to": employee_token["user_id"],
        "priority": "high"
    }
    await client.post("/api/tasks", json=task_data, headers=lead_headers)
    
    # Employee uses AI to list tasks
    emp_headers = auth_headers(employee_token["token"])
    
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        mock_response = """{
            "thought": "Listing user's tasks",
            "actions": [
                {
                    "name": "list_user_tasks",
                    "params": {}
                }
            ]
        }"""
        mock_instance.send_message = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Show my tasks",
            "session_id": "test-session-action"
        }
        
        response = await client.post("/api/ai/execute", json=ai_request, headers=emp_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that action was executed
        assert len(data["actionsExecuted"]) == 1
        executed_action = data["actionsExecuted"][0]
        assert executed_action["action"] == "list_user_tasks"
        assert executed_action["success"] is True


@pytest.mark.asyncio
async def test_ai_without_llm_key(client, employee_token):
    """Test AI endpoints when EMERGENT_LLM_KEY is not configured"""
    headers = auth_headers(employee_token["token"])
    
    # Mock environment to simulate missing key
    with patch('server.os.environ.get', return_value=None):
        ai_request = {
            "message": "Test without key",
            "session_id": "test-no-key"
        }
        
        response = await client.post("/api/ai/chat", json=ai_request, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "error" in data or "unavailable" in data["response"].lower()


@pytest.mark.asyncio
async def test_ai_execute_multiple_actions(client, employee_token):
    """Test AI can execute multiple actions in sequence"""
    headers = auth_headers(employee_token["token"])
    
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        mock_response = """{
            "thought": "Summarizing tasks and notifications",
            "actions": [
                {
                    "name": "summarize_tasks",
                    "params": {}
                },
                {
                    "name": "summarize_notifications",
                    "params": {}
                }
            ]
        }"""
        mock_instance.send_message = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Give me a full summary",
            "session_id": "test-multi-action"
        }
        
        response = await client.post("/api/ai/execute", json=ai_request, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have executed 2 actions
        assert len(data["actionsExecuted"]) == 2


@pytest.mark.asyncio
async def test_ai_chat_saves_to_database(client, employee_token, test_db):
    """Test that AI chat messages are saved to database"""
    headers = auth_headers(employee_token["token"])
    
    with patch('server.LlmChat') as mock_llm_class:
        mock_instance = AsyncMock()
        mock_instance.send_message = AsyncMock(return_value="Test response")
        mock_llm_class.return_value = mock_instance
        
        ai_request = {
            "message": "Test message for DB",
            "session_id": "test-db-save"
        }
        
        await client.post("/api/ai/chat", json=ai_request, headers=headers)
        
        # Check database
        messages = await test_db.ai_messages.find({
            "user_id": employee_token["user_id"],
            "session_id": "test-db-save"
        }).to_list(10)
        
        assert len(messages) == 1
        assert messages[0]["message"] == "Test message for DB"
        assert messages[0]["response"] == "Test response"
        assert messages[0]["action_type"] == "chat"


@pytest.mark.asyncio
async def test_ai_history_endpoint(client, employee_token, test_db):
    """Test retrieving AI conversation history"""
    headers = auth_headers(employee_token["token"])
    
    # Insert some AI messages directly to DB
    session_id = "test-history-session"
    messages = [
        {
            "id": "msg1",
            "user_id": employee_token["user_id"],
            "session_id": session_id,
            "message": "First message",
            "response": "First response",
            "action_type": "chat",
            "actions_executed": [],
            "created_at": "2025-01-01T10:00:00Z"
        },
        {
            "id": "msg2",
            "user_id": employee_token["user_id"],
            "session_id": session_id,
            "message": "Second message",
            "response": "Second response",
            "action_type": "chat",
            "actions_executed": [],
            "created_at": "2025-01-01T10:05:00Z"
        }
    ]
    await test_db.ai_messages.insert_many(messages)
    
    # Get history
    response = await client.get(f"/api/ai/history?session_id={session_id}", headers=headers)
    
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2
    assert history[0]["message"] == "First message"
    assert history[1]["message"] == "Second message"
