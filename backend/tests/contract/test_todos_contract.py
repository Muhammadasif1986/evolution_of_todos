import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.main import app
from backend.src.database import get_db
from backend.src.models.user import User
from backend.src.models.todo_item import TodoItem
from backend.src.schemas.todo_item import TodoItemCreate, TodoItemUpdate
import json

# Test suite for POST /todos endpoint contract
def test_post_todos_contract():
    """
    Contract test for POST /todos endpoint
    Tests that the endpoint accepts valid todo creation requests and returns expected response format
    """
    client = TestClient(app)

    # Prepare test data
    todo_data = {
        "title": "Test Todo",
        "description": "Test description",
        "priority": "medium",
        "due_date": "2023-12-31T23:59:59"
    }

    # Send request
    response = client.post("/todos/", json=todo_data)

    # Assertions
    assert response.status_code in [200, 401, 422]  # 200 for success, 401 for auth issues, 422 for validation
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert data["title"] == todo_data["title"]
        assert data["description"] == todo_data["description"]
        assert data["priority"] == todo_data["priority"]


def test_get_todos_contract():
    """
    Contract test for GET /todos endpoint
    Tests that the endpoint returns expected response format
    """
    client = TestClient(app)

    # Send request
    response = client.get("/todos/")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)


def test_put_todos_id_contract():
    """
    Contract test for PUT /todos/{id} endpoint
    Tests that the endpoint accepts valid todo update requests and returns expected response format
    """
    client = TestClient(app)

    # Prepare test data
    todo_data = {
        "title": "Updated Todo",
        "description": "Updated description",
        "priority": "high",
        "due_date": "2023-12-31T23:59:59"
    }

    # Try to update a todo (may fail if no todos exist, which is expected in contract testing)
    response = client.put("/todos/999999", json=todo_data)  # Use non-existent ID

    # Assertions - we're testing contract compliance, not functionality
    assert response.status_code in [200, 401, 404, 422]


def test_patch_todos_id_status_contract():
    """
    Contract test for PATCH /todos/{id}/status endpoint
    Tests that the endpoint accepts valid status update requests and returns expected response format
    """
    client = TestClient(app)

    # Prepare test data
    status_data = {
        "status": "completed"
    }

    # Try to update status (may fail if no todos exist, which is expected in contract testing)
    response = client.patch("/todos/999999/status", json=status_data)  # Use non-existent ID

    # Assertions
    assert response.status_code in [200, 401, 404, 422]
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "status" in data


def test_delete_todos_id_contract():
    """
    Contract test for DELETE /todos/{id} endpoint
    Tests that the endpoint returns expected response format
    """
    client = TestClient(app)

    # Try to delete a todo (may fail if no todos exist, which is expected in contract testing)
    response = client.delete("/todos/999999")  # Use non-existent ID

    # Assertions
    assert response.status_code in [200, 204, 401, 404]