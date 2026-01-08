import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_get_todos_sort_by_due_date_contract():
    """
    Contract test for GET /todos sorting by due_date
    Tests that the endpoint accepts due_date sort parameter and returns expected response format
    """
    # Send request with due_date sort parameter
    response = client.get("/todos/?sort=due_date")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)


def test_get_todos_sort_by_created_at_contract():
    """
    Contract test for GET /todos sorting by created_at
    Tests that the endpoint accepts created_at sort parameter and returns expected response format
    """
    # Send request with created_at sort parameter
    response = client.get("/todos/?sort=created_at")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)


def test_get_todos_sort_by_priority_contract():
    """
    Contract test for GET /todos sorting by priority
    Tests that the endpoint accepts priority sort parameter and returns expected response format
    """
    # Send request with priority sort parameter
    response = client.get("/todos/?sort=priority")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)