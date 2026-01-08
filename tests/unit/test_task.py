'''
Unit tests for Task model in the Todo Console App
'''
import pytest
from datetime import datetime
from src.models.task import Task


class TestTask:
    """Unit tests for the Task model."""

    def test_task_creation_with_required_fields(self):
        """Test creating a task with required fields."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields."""
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=True,
            created_at=test_datetime
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is True
        assert task.created_at == test_datetime

    def test_task_creation_auto_timestamp(self):
        """Test that created_at is automatically set if not provided."""
        task = Task(id=1, title="Test Task")

        assert isinstance(task.created_at, datetime)
        # Check that the timestamp is reasonably close to now
        time_diff = abs((datetime.now() - task.created_at).total_seconds())
        assert time_diff < 1  # Should be within 1 second

    def test_task_validation_valid_title(self):
        """Test that validation passes with a valid title."""
        task = Task(id=1, title="Valid Title")

        # Should not raise an exception
        task.validate()

    def test_task_validation_empty_title(self):
        """Test that validation fails with an empty title."""
        task = Task(id=1, title="")

        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            task.validate()

    def test_task_validation_whitespace_only_title(self):
        """Test that validation fails with a whitespace-only title."""
        task = Task(id=1, title="   ")

        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            task.validate()

    def test_task_validation_none_title(self):
        """Test that validation fails with a None title."""
        # Note: This test might not be applicable depending on how Task handles None values
        # Since we're using dataclasses, None values would be passed directly
        # This test is more about ensuring the validation logic works as expected
        task = Task(id=1, title=None)

        # This should raise an error since None will fail the truthiness check
        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            task.validate()