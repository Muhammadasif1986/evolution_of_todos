import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_get_todos_with_multiple_query_parameters_contract():
    """
    Contract test for GET /todos with multiple query parameters
    Tests that the endpoint accepts multiple query parameters and returns expected response format
    """
    # Send request with multiple query parameters
    response = client.get("/todos/?status=pending&priority=high&sort=due_date&limit=10&offset=0")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        # Response should be a list of todo items


def test_get_todos_with_status_and_priority_filter_contract():
    """
    Contract test for GET /todos with status and priority filters
    Tests that the endpoint accepts status and priority parameters and returns expected response format
    """
    # Send request with status and priority filters
    response = client.get("/todos/?status=completed&priority=low")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)


def test_get_todos_with_limit_offset_contract():
    """
    Contract test for GET /todos with limit and offset parameters
    Tests that the endpoint accepts pagination parameters and returns expected response format
    """
    # Send request with pagination parameters
    response = client.get("/todos/?limit=5&offset=10")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        # Length should be <= limit (if enough todos exist)