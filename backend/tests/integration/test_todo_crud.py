import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import get_db, engine, Base
from backend.src.models.user import User
from backend.src.models.todo_item import TodoItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import json

# Create a test database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
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

def test_todo_crud_journey():
    """
    Integration test for todo CRUD journey
    Tests the complete flow of creating, reading, updating, and deleting a todo item
    """
    # First, we need to register and login a user to get a valid token
    # Register a user
    registration_data = {
        "email": "integration_test@example.com",
        "password": "securePassword123",
        "username": "integration_test_user"
    }
    response = client.post("/auth/register", json=registration_data)
    assert response.status_code in [200, 400]  # May fail if user already exists

    # Login to get a token
    login_data = {
        "email": "integration_test@example.com",
        "password": "securePassword123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Set up headers with the token
    headers = {"Authorization": f"Bearer {access_token}"}

    # CREATE: Create a new todo
    todo_data = {
        "title": "Integration Test Todo",
        "description": "This is a test todo for integration testing",
        "priority": "medium"
    }
    response = client.post("/todos/", json=todo_data, headers=headers)
    assert response.status_code == 200
    created_todo = response.json()
    assert created_todo["title"] == todo_data["title"]
    assert created_todo["description"] == todo_data["description"]
    assert created_todo["status"] == "pending"
    todo_id = created_todo["id"]

    # READ: Get the created todo
    response = client.get(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 200
    retrieved_todo = response.json()
    assert retrieved_todo["id"] == todo_id
    assert retrieved_todo["title"] == todo_data["title"]

    # UPDATE: Update the todo
    update_data = {
        "title": "Updated Integration Test Todo",
        "description": "Updated description for integration testing",
        "priority": "high"
    }
    response = client.put(f"/todos/{todo_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == update_data["title"]
    assert updated_todo["description"] == update_data["description"]

    # UPDATE: Change status to completed
    status_data = {"status": "completed"}
    response = client.patch(f"/todos/{todo_id}/status", json=status_data, headers=headers)
    assert response.status_code == 200
    status_updated_todo = response.json()
    assert status_updated_todo["id"] == todo_id
    assert status_updated_todo["status"] == "completed"

    # READ: Get all todos and verify our todo is in the list
    response = client.get("/todos/", headers=headers)
    assert response.status_code == 200
    todos = response.json()
    todo_ids = [todo["id"] for todo in todos]
    assert todo_id in todo_ids

    # DELETE: Delete the todo
    response = client.delete(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 200  # or 204

    # VERIFY: Try to get the deleted todo (should fail)
    response = client.get(f"/todos/{todo_id}", headers=headers)
    assert response.status_code in [404]  # Todo should no longer exist