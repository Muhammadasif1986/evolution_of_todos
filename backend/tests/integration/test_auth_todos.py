import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import get_db, engine, Base
from backend.src.models.user import User
from backend.src.models.todo_item import TodoItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

# Create a test database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_todos.db"
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

def test_todo_access_control():
    """
    Integration test for todo access control
    Tests that users can only access their own todos and not others'
    """
    # Register first user
    user1_data = {
        "email": "user1@example.com",
        "password": "SecurePassword123!",
        "username": "user1"
    }
    response = client.post("/auth/register", json=user1_data)
    # May return 200 for new user or 400 if user already exists
    assert response.status_code in [200, 400]

    # Register second user
    user2_data = {
        "email": "user2@example.com",
        "password": "SecurePassword123!",
        "username": "user2"
    }
    response = client.post("/auth/register", json=user2_data)
    assert response.status_code in [200, 400]

    # Login as first user
    login_data = {
        "email": "user1@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    user1_token = response.json()["access_token"]

    # Login as second user
    login_data = {
        "email": "user2@example.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    user2_token = response.json()["access_token"]

    # Set up headers
    user1_headers = {"Authorization": f"Bearer {user1_token}"}
    user2_headers = {"Authorization": f"Bearer {user2_token}"}

    # User 1 creates a todo
    todo_data = {
        "title": "User 1's Private Todo",
        "description": "This should only be accessible to user 1",
        "priority": "medium"
    }
    response = client.post("/todos/", json=todo_data, headers=user1_headers)
    assert response.status_code == 200
    user1_todo = response.json()
    user1_todo_id = user1_todo["id"]
    assert "id" in user1_todo

    # User 1 should be able to access their own todo
    response = client.get(f"/todos/{user1_todo_id}", headers=user1_headers)
    assert response.status_code == 200

    # User 2 should NOT be able to access user 1's todo
    response = client.get(f"/todos/{user1_todo_id}", headers=user2_headers)
    # This should return 403 (Forbidden) or 404 (Not Found) to prevent ID enumeration
    assert response.status_code in [403, 404]

    # User 1 should see their todo in their todo list
    response = client.get("/todos/", headers=user1_headers)
    assert response.status_code == 200
    user1_todos = response.json()
    user1_todo_ids = [todo["id"] for todo in user1_todos]
    assert user1_todo_id in user1_todo_ids

    # User 2 should NOT see user 1's todo in their list
    response = client.get("/todos/", headers=user2_headers)
    assert response.status_code == 200
    user2_todos = response.json()
    user2_todo_ids = [todo["id"] for todo in user2_todos]
    assert user1_todo_id not in user2_todo_ids

    # User 2 tries to update user 1's todo (should fail)
    update_data = {
        "title": "Attempted Update by User 2",
        "description": "This should fail",
        "priority": "high"
    }
    response = client.put(f"/todos/{user1_todo_id}", json=update_data, headers=user2_headers)
    assert response.status_code in [403, 404]

    # User 2 tries to delete user 1's todo (should fail)
    response = client.delete(f"/todos/{user1_todo_id}", headers=user2_headers)
    assert response.status_code in [403, 404]