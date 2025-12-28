'''
Integration tests for CLI functionality in the Todo Console App
'''
import pytest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from src.cli.main import TodoCLI


class TestCLIIntegration:
    """Integration tests for the CLI functionality."""

    @patch('builtins.input')
    def test_add_task_via_cli(self, mock_input):
        """Test adding a task via CLI interface."""
        cli = TodoCLI()

        # Mock user input for adding a task
        mock_input.side_effect = ["1", "New Task", "Description for new task", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task was added by checking the service
        tasks = cli.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "New Task"
        assert tasks[0].description == "Description for new task"
        assert tasks[0].completed is False

    @patch('builtins.input')
    def test_add_task_empty_title_validation(self, mock_input):
        """Test that CLI properly validates empty task titles."""
        cli = TodoCLI()

        # Mock user input for adding a task with empty title
        mock_input.side_effect = ["1", "", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify no tasks were added
        tasks = cli.service.get_all_tasks()
        assert len(tasks) == 0

        # Verify error message was displayed
        output = output_buffer.getvalue()
        assert "Task title cannot be empty" in output or "Task title must not be empty" in output

    @patch('builtins.input')
    def test_view_tasks_via_cli(self, mock_input):
        """Test viewing tasks via CLI interface."""
        cli = TodoCLI()

        # Add a task first
        cli.service.add_task("Test Task", "Test Description")

        # Mock user input for viewing tasks
        mock_input.side_effect = ["2", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task appears in the output
        output = output_buffer.getvalue()
        assert "Test Task" in output
        assert "Test Description" in output

    @patch('builtins.input')
    def test_complete_task_via_cli(self, mock_input):
        """Test marking a task as complete via CLI interface."""
        cli = TodoCLI()

        # Add a task first
        task = cli.service.add_task("Test Task", "Test Description")

        # Mock user input for marking task as complete
        mock_input.side_effect = ["3", "1", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task is now marked as complete
        updated_task = cli.service.get_task(task.id)
        assert updated_task.completed is True

    @patch('builtins.input')
    def test_update_task_via_cli(self, mock_input):
        """Test updating a task via CLI interface."""
        cli = TodoCLI()

        # Add a task first
        task = cli.service.add_task("Old Title", "Old Description")

        # Mock user input for updating the task
        mock_input.side_effect = ["4", "1", "New Title", "New Description", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task was updated
        updated_task = cli.service.get_task(task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    @patch('builtins.input')
    def test_delete_task_via_cli(self, mock_input):
        """Test deleting a task via CLI interface."""
        cli = TodoCLI()

        # Add a task first
        task = cli.service.add_task("Test Task", "Test Description")

        # Mock user input for deleting the task
        mock_input.side_effect = ["5", "1", "y", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task was deleted
        tasks = cli.service.get_all_tasks()
        assert len(tasks) == 0

    @patch('builtins.input')
    def test_view_tasks_empty_list(self, mock_input):
        """Test viewing tasks when the list is empty."""
        cli = TodoCLI()

        # Mock user input for viewing tasks when empty
        mock_input.side_effect = ["2", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify appropriate message is shown
        output = output_buffer.getvalue()
        assert "No tasks found" in output or "0 tasks" in output.lower()

    @patch('builtins.input')
    def test_view_tasks_with_completed_and_pending(self, mock_input):
        """Test viewing tasks with both completed and pending tasks."""
        cli = TodoCLI()

        # Add tasks and mark one as complete
        pending_task = cli.service.add_task("Pending Task", "Description for pending task")
        completed_task = cli.service.add_task("Completed Task", "Description for completed task")
        cli.service.toggle_task_status(completed_task.id)

        # Mock user input for viewing tasks
        mock_input.side_effect = ["2", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify both tasks appear in the output with correct status indicators
        output = output_buffer.getvalue()
        assert "Pending Task" in output
        assert "Completed Task" in output
        # Check for status indicators
        assert "○" in output  # Pending indicator
        assert "✓" in output  # Completed indicator

    @patch('builtins.input')
    def test_mark_task_complete_via_cli(self, mock_input):
        """Test marking a task as complete via CLI interface."""
        cli = TodoCLI()

        # Add a task first
        task = cli.service.add_task("Test Task", "Test Description")
        assert task.completed is False  # Initially pending

        # Mock user input for marking task as complete
        mock_input.side_effect = ["3", "1", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task is now marked as complete
        updated_task = cli.service.get_task(task.id)
        assert updated_task.completed is True

    @patch('builtins.input')
    def test_mark_task_incomplete_via_cli(self, mock_input):
        """Test marking a completed task as incomplete via CLI interface."""
        cli = TodoCLI()

        # Add a task and mark it as complete first
        task = cli.service.add_task("Test Task", "Test Description")
        cli.service.toggle_task_status(task.id)  # Mark as complete
        assert task.completed is True

        # Mock user input for marking task as incomplete
        mock_input.side_effect = ["3", "1", "6"]

        # Capture output
        output_buffer = StringIO()

        with redirect_stdout(output_buffer):
            cli.run()

        # Verify the task is now marked as incomplete
        updated_task = cli.service.get_task(task.id)
        assert updated_task.completed is False

