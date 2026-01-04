import pytest
from backend.src.models.todo_item import TodoItem
from backend.src.models.user import User
from datetime import datetime

def test_todo_item_model():
    """
    Unit test for TodoItem model
    """
    todo = TodoItem(
        title="Test Todo",
        description="Test description",
        status="pending",
        priority="medium",
        user_id=1
    )

    assert todo.title == "Test Todo"
    assert todo.description == "Test description"
    assert todo.status == "pending"
    assert todo.priority == "medium"
    assert todo.user_id == 1
    assert todo.id is None  # ID will be set by the database


def test_user_model():
    """
    Unit test for User model
    """
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password_here"
    )

    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password == "hashed_password_here"
    assert user.id is None  # ID will be set by the database
    assert user.is_active == True


def test_todo_item_default_values():
    """
    Unit test for TodoItem model default values
    """
    todo = TodoItem(
        title="Test Todo",
        user_id=1
    )

    # Check if defaults are properly set
    assert todo.title == "Test Todo"
    assert todo.status == "pending"  # Should be default
    assert todo.priority == "medium"  # Should be default
    assert todo.user_id == 1