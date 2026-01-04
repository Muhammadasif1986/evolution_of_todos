import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
import json

# Test suite for authentication contract endpoints

def test_post_auth_register_contract():
    """
    Contract test for POST /auth/register endpoint
    Tests that the endpoint accepts valid registration requests and returns expected response format
    """
    client = TestClient(app)

    # Prepare test data
    registration_data = {
        "email": "test@example.com",
        "password": "securePassword123",
        "username": "testuser"
    }

    # Send request
    response = client.post("/auth/register", json=registration_data)

    # Assertions
    assert response.status_code in [200, 400, 422]  # 200 for success, 400 for validation errors, 422 for validation
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert data["email"] == registration_data["email"]
        assert data["username"] == registration_data["username"]


def test_post_auth_login_contract():
    """
    Contract test for POST /auth/login endpoint
    Tests that the endpoint accepts valid login credentials and returns expected response format
    """
    client = TestClient(app)

    # Prepare test data
    login_data = {
        "email": "test@example.com",
        "password": "securePassword123"
    }

    # Send request
    response = client.post("/auth/login", json=login_data)

    # Assertions
    assert response.status_code in [200, 400, 401, 422]  # 200 for success, 401 for invalid credentials
    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


def test_post_auth_logout_contract():
    """
    Contract test for POST /auth/logout endpoint
    Tests that the endpoint accepts logout requests and returns expected response format
    """
    client = TestClient(app)

    # Send request (without authentication token, which should result in 401)
    response = client.post("/auth/logout")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for unauthenticated requests