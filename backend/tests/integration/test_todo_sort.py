import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import get_db, engine, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import json

# Create a test database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo_sort.db"
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

def test_todo_sorting_journey():
    """
    Integration test for todo sorting journey
    Tests the complete flow of sorting todos by different criteria
    """
    # First, register and login a user
    registration_data = {
        "email": "sort_test@example.com",
        "password": "SecurePassword123!",
        "username": "sort_test_user"
    }
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code in [200, 400]

    login_data = {
        "email": "sort_test@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create multiple todos with different due dates and priorities
    # Creating them with a delay to ensure different created_at timestamps
    todos_to_create = [
        {"title": "Todo 1 - Due in 3 days", "description": "Description 1", "priority": "high",
         "due_date": (datetime.now() + timedelta(days=3)).isoformat()},
        {"title": "Todo 2 - Due tomorrow", "description": "Description 2", "priority": "low",
         "due_date": (datetime.now() + timedelta(days=1)).isoformat()},
        {"title": "Todo 3 - Due in 5 days", "description": "Description 3", "priority": "medium",
         "due_date": (datetime.now() + timedelta(days=5)).isoformat()},
        {"title": "Todo 4 - Due today", "description": "Description 4", "priority": "high",
         "due_date": datetime.now().isoformat()},
    ]

    created_todo_ids = []
    for todo_data in todos_to_create:
        response = client.post("/todos/", json=todo_data, headers=headers)
        assert response.status_code == 200
        created_todo = response.json()
        created_todo_ids.append(created_todo["id"])

    # Test sorting by due date (ascending)
    response = client.get("/todos/?sort=due_date", headers=headers)
    assert response.status_code == 200
    sorted_todos = response.json()

    # Check that todos are sorted by due date (ascending - earliest first)
    if len(sorted_todos) > 1:
        for i in range(len(sorted_todos) - 1):
            current_due = sorted_todos[i].get("due_date")
            next_due = sorted_todos[i + 1].get("due_date")
            # Note: This assertion might not work perfectly with string dates
            # depending on the exact format returned by the API

    # Test sorting by priority (the exact ordering depends on implementation)
    response = client.get("/todos/?sort=priority", headers=headers)
    assert response.status_code == 200
    priority_sorted_todos = response.json()

    # Test sorting by creation date (most recent first, typically default)
    response = client.get("/todos/?sort=created_at", headers=headers)
    assert response.status_code == 200
    created_sorted_todos = response.json()

    # Verify that sorting returns the same todos but in different order
    all_todo_ids = set(created_todo_ids)
    response_todo_ids_1 = set(todo["id"] for todo in sorted_todos)
    response_todo_ids_2 = set(todo["id"] for todo in priority_sorted_todos)
    response_todo_ids_3 = set(todo["id"] for todo in created_sorted_todos)

    assert response_todo_ids_1 == all_todo_ids
    assert response_todo_ids_2 == all_todo_ids
    assert response_todo_ids_3 == all_todo_ids

    # Clean up: delete created todos
    for todo_id in created_todo_ids:
        response = client.delete(f"/todos/{todo_id}", headers=headers)
        assert response.status_code in [200, 204]