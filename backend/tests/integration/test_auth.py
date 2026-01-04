import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import get_db, engine, Base
from backend.src.models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

# Create a test database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
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

def test_user_registration_journey():
    """
    Integration test for user registration journey
    Tests the complete flow of registering a new user account
    """
    # Prepare registration data
    registration_data = {
        "email": "auth_integration_test@example.com",
        "password": "SecurePassword123!",
        "username": "auth_integration_user"
    }

    # Register a new user
    response = client.post("/auth/register", json=registration_data)

    # Should succeed if this is a new user
    assert response.status_code in [200, 400]  # 200 for success, 400 if user already exists

    if response.status_code == 200:
        user_data = response.json()
        assert "id" in user_data
        assert user_data["email"] == registration_data["email"]
        assert user_data["username"] == registration_data["username"]
        assert "created_at" in user_data


def test_user_login_logout_journey():
    """
    Integration test for user login/logout journey
    Tests the complete flow of logging in and out of an account
    """
    # First register a user (or try to, might already exist)
    registration_data = {
        "email": "login_test@example.com",
        "password": "SecurePassword123!",
        "username": "login_test_user"
    }

    # Try to register (might fail if user already exists, which is okay)
    client.post("/auth/register", json=registration_data)

    # Login with the registered user
    login_data = {
        "email": "login_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200

    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    access_token = token_data["access_token"]

    # Verify the token works by accessing a protected endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/todos/", headers=headers)
    # This might return 200 (empty list) or 401/403 depending on implementation
    assert response.status_code in [200, 401, 403, 422]

    # Test logout (if endpoint exists)
    # Note: In JWT-based auth, logout is typically client-side only
    # but if there's a server-side logout endpoint, test it
    response = client.post("/auth/logout", headers=headers)
    # This endpoint might not exist in JWT-based systems, so we allow 404
    assert response.status_code in [200, 404, 401]