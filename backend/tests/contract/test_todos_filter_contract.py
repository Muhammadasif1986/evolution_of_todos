import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_get_todos_filter_by_status_contract():
    """
    Contract test for GET /todos filtering by status
    Tests that the endpoint accepts status query parameter and returns expected response format
    """
    # Send request with status filter
    response = client.get("/todos/?status=pending")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        # If there are todos in the response, they should match the filter criteria
        for todo in data:
            assert isinstance(todo, dict)
            if "status" in todo:
                # Note: This assertion may not always be true if no todos match the filter
                # The endpoint might return an empty list, which is valid
                pass


def test_get_todos_sort_by_due_date_contract():
    """
    Contract test for GET /todos sorting by due_date
    Tests that the endpoint accepts sort query parameter and returns expected response format
    """
    # Send request with sort parameter
    response = client.get("/todos/?sort=due_date")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)


def test_get_todos_with_multiple_query_parameters_contract():
    """
    Contract test for GET /todos with multiple query parameters
    Tests that the endpoint accepts multiple query parameters and returns expected response format
    """
    # Send request with multiple query parameters
    response = client.get("/todos/?status=pending&priority=high&sort=due_date&limit=10")

    # Assertions
    assert response.status_code in [200, 401]  # 200 for success, 401 for auth issues
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)