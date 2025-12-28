'''
Unit tests for TodoService in the Todo Console App
'''
import pytest
from src.services.todo_service import TodoService
from src.models.task import Task


class TestTodoService:
    """Unit tests for the TodoService."""

    def test_initialization(self):
        """Test that TodoService initializes correctly."""
        service = TodoService()

        assert service._tasks == {}
        assert service._next_id == 1

    def test_add_task_success(self):
        """Test adding a task successfully."""
        service = TodoService()
        task = service.add_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert len(service._tasks) == 1
        assert service._next_id == 2

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        service = TodoService()
        task = service.add_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_empty_title(self):
        """Test that adding a task with empty title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            service.add_task("")

    def test_add_task_whitespace_only_title(self):
        """Test that adding a task with whitespace-only title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            service.add_task("   ")

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when list is empty."""
        service = TodoService()
        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_multiple(self):
        """Test getting all tasks when multiple tasks exist."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        # Tasks should be sorted by ID
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_task_success(self):
        """Test getting a specific task by ID."""
        service = TodoService()
        added_task = service.add_task("Test Task")
        retrieved_task = service.get_task(added_task.id)

        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title
        assert retrieved_task.description == added_task.description

    def test_get_task_nonexistent(self):
        """Test that getting a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.get_task(999)

    def test_update_task_title_success(self):
        """Test updating a task's title successfully."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, title="New Title")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_description_success(self):
        """Test updating a task's description successfully."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, description="New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "Original Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_both_fields_success(self):
        """Test updating both title and description successfully."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, title="New Title", description="New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_nonexistent(self):
        """Test that updating a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.update_task(999, title="New Title")

    def test_update_task_empty_title(self):
        """Test that updating to an empty title raises ValueError."""
        service = TodoService()
        original_task = service.add_task("Original Title")

        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            service.update_task(original_task.id, title="")

    def test_toggle_task_status_success(self):
        """Test toggling a task's status successfully."""
        service = TodoService()
        task = service.add_task("Test Task")
        # Initially should be False
        assert task.completed is False

        toggled_task = service.toggle_task_status(task.id)
        # Should now be True
        assert toggled_task.completed is True

        toggled_task2 = service.toggle_task_status(task.id)
        # Should now be False again
        assert toggled_task2.completed is False

    def test_toggle_task_status_nonexistent(self):
        """Test that toggling a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.toggle_task_status(999)

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        service = TodoService()
        task = service.add_task("Test Task")

        result = service.delete_task(task.id)

        assert result is True
        assert len(service._tasks) == 0

    def test_delete_task_nonexistent(self):
        """Test that deleting a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.delete_task(999)

    def test_task_ids_remain_unique(self):
        """Test that task IDs remain unique after various operations."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        service.delete_task(task1.id)
        task3 = service.add_task("Task 3")

        # All remaining tasks should have unique IDs
        tasks = service.get_all_tasks()
        ids = [task.id for task in tasks]
        assert len(ids) == len(set(ids))  # Check uniqueness

    def test_get_all_tasks_empty(self):
        """Test that get_all_tasks returns empty list when no tasks exist."""
        service = TodoService()
        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_sorted_by_id(self):
        """Test that get_all_tasks returns tasks sorted by ID."""
        service = TodoService()
        task3 = service.add_task("Task 3")
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        tasks = service.get_all_tasks()

        # Should be sorted by ID: 1, 2, 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_task_success(self):
        """Test that get_task returns the correct task."""
        service = TodoService()
        original_task = service.add_task("Test Task", "Test Description")

        retrieved_task = service.get_task(original_task.id)

        assert retrieved_task.id == original_task.id
        assert retrieved_task.title == original_task.title
        assert retrieved_task.description == original_task.description
        assert retrieved_task.completed == original_task.completed

    def test_get_task_nonexistent_raises_error(self):
        """Test that get_task raises ValueError for non-existent task."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.get_task(999)

    def test_toggle_task_status_success(self):
        """Test toggling a task's status successfully."""
        service = TodoService()
        task = service.add_task("Test Task")
        # Initially should be False
        assert task.completed is False

        toggled_task = service.toggle_task_status(task.id)
        # Should now be True
        assert toggled_task.completed is True

        toggled_task2 = service.toggle_task_status(task.id)
        # Should now be False again
        assert toggled_task2.completed is False

    def test_toggle_task_status_nonexistent(self):
        """Test that toggling a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.toggle_task_status(999)

    def test_update_task_title_success(self):
        """Test updating a task's title successfully."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, title="New Title")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_description_success(self):
        """Test updating a task's description successfully."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, description="New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "Original Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_both_fields_success(self):
        """Test updating both title and description successfully."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, title="New Title", description="New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_nonexistent(self):
        """Test that updating a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.update_task(999, title="New Title")

    def test_update_task_empty_title(self):
        """Test that updating to an empty title raises ValueError."""
        service = TodoService()
        original_task = service.add_task("Original Title")

        with pytest.raises(ValueError, match="Task title must not be empty or contain only whitespace"):
            service.update_task(original_task.id, title="")

    def test_update_task_none_values_no_change(self):
        """Test that passing None values doesn't change those fields."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")
        original_completed = original_task.completed

        updated_task = service.update_task(original_task.id, title=None, description=None)

        assert updated_task.id == original_task.id
        assert updated_task.title == "Original Title"
        assert updated_task.description == "Original Description"
        assert updated_task.completed == original_completed

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        service = TodoService()
        task = service.add_task("Test Task")

        result = service.delete_task(task.id)

        assert result is True
        assert len(service._tasks) == 0
        # Verify the task is no longer accessible
        with pytest.raises(ValueError):
            service.get_task(task.id)

    def test_delete_task_nonexistent(self):
        """Test that deleting a non-existent task raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.delete_task(999)

    def test_task_ids_remain_unique_after_deletion(self):
        """Test that task IDs remain unique after deletion operations."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        service.delete_task(task1.id)
        task3 = service.add_task("Task 3")

        # All remaining tasks should have unique IDs
        tasks = service.get_all_tasks()
        ids = [task.id for task in tasks]
        assert len(ids) == len(set(ids))  # Check uniqueness
        # IDs should still be 2 and 3
        assert set(ids) == {2, 3}