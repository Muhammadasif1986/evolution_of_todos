import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import get_db, engine, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

# Create a test database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo_filter.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create the tables
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_todo_filtering_journey():
    """
    Integration test for todo filtering journey
    Tests the complete flow of filtering todos by different criteria
    """
    # First, register and login a user
    registration_data = {
        "email": "filter_test@example.com",
        "password": "SecurePassword123!",
        "username": "filter_test_user"
    }
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code in [200, 400]

    login_data = {
        "email": "filter_test@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create multiple todos with different statuses and priorities
    todos_to_create = [
        {"title": "High Priority Pending Todo", "description": "Description 1", "priority": "high", "status": "pending"},
        {"title": "Medium Priority Pending Todo", "description": "Description 2", "priority": "medium", "status": "pending"},
        {"title": "Low Priority Completed Todo", "description": "Description 3", "priority": "low", "status": "completed"},
        {"title": "High Priority Completed Todo", "description": "Description 4", "priority": "high", "status": "completed"},
    ]

    created_todo_ids = []
    for todo_data in todos_to_create:
        # Note: The status might be set to "pending" by default in the backend
        # so we'll create them and then update the status for completed ones
        response = client.post("/todos/", json=todo_data, headers=headers)
        assert response.status_code == 200
        created_todo = response.json()
        created_todo_ids.append(created_todo["id"])

    # Update the status of some todos to "completed"
    for i in [2, 3]:  # Indices of todos that should be completed
        response = client.patch(f"/todos/{created_todo_ids[i]}/status",
                               json={"status": "completed"}, headers=headers)
        assert response.status_code == 200

    # Test filtering by status: get only pending todos
    response = client.get("/todos/?status=pending", headers=headers)
    assert response.status_code == 200
    pending_todos = response.json()
    pending_todo_ids = [todo["id"] for todo in pending_todos]

    # Verify that only pending todos are returned
    assert created_todo_ids[0] in pending_todo_ids  # High priority pending
    assert created_todo_ids[1] in pending_todo_ids  # Medium priority pending
    assert created_todo_ids[2] not in pending_todo_ids  # Low priority completed
    assert created_todo_ids[3] not in pending_todo_ids  # High priority completed

    # Test filtering by status: get only completed todos
    response = client.get("/todos/?status=completed", headers=headers)
    assert response.status_code == 200
    completed_todos = response.json()
    completed_todo_ids = [todo["id"] for todo in completed_todos]

    # Verify that only completed todos are returned
    assert created_todo_ids[0] not in completed_todo_ids  # High priority pending
    assert created_todo_ids[1] not in completed_todo_ids  # Medium priority pending
    assert created_todo_ids[2] in completed_todo_ids  # Low priority completed
    assert created_todo_ids[3] in completed_todo_ids  # High priority completed

    # Test filtering by priority: get only high priority todos
    response = client.get("/todos/?priority=high", headers=headers)
    assert response.status_code == 200
    high_priority_todos = response.json()
    high_priority_todo_ids = [todo["id"] for todo in high_priority_todos]

    # Verify that only high priority todos are returned
    assert created_todo_ids[0] in high_priority_todo_ids  # High priority pending
    assert created_todo_ids[3] in high_priority_todo_ids  # High priority completed
    assert created_todo_ids[1] not in high_priority_todo_ids  # Medium priority
    assert created_todo_ids[2] not in high_priority_todo_ids  # Low priority

    # Test filtering by multiple criteria: high priority AND completed
    response = client.get("/todos/?priority=high&status=completed", headers=headers)
    assert response.status_code == 200
    high_priority_completed_todos = response.json()
    high_priority_completed_ids = [todo["id"] for todo in high_priority_completed_todos]

    # Verify that only high priority completed todos are returned
    assert created_todo_ids[3] in high_priority_completed_ids  # High priority completed
    assert created_todo_ids[0] not in high_priority_completed_ids  # High priority pending
    assert created_todo_ids[1] not in high_priority_completed_ids  # Medium priority pending
    assert created_todo_ids[2] not in high_priority_completed_ids  # Low priority completed

    # Clean up: delete created todos
    for todo_id in created_todo_ids:
        response = client.delete(f"/todos/{todo_id}", headers=headers)
        assert response.status_code in [200, 204]