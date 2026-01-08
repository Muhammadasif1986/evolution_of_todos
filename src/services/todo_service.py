'''
TodoService for the Todo Console App
'''
import os
import sys
from typing import List, Optional
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.task import Task


class TodoService:
    """
    Core business logic for task management.
    Implements the service contracts defined in the specification.
    """

    def __init__(self):
        """Initialize the service with an empty task list and ID counter."""
        self._tasks = {}  # Dictionary to store tasks by ID
        self._next_id = 1  # Counter for generating unique task IDs

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the todo list.

        Args:
            title (str): Required task title (min 1 char)
            description (str): Optional task description

        Returns:
            Task: Task object with assigned ID and creation timestamp

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        # Validate input - this implements the validation required in T011
        if not title or not title.strip():
            raise ValueError("Task title must not be empty or contain only whitespace")

        # Create new task with unique ID
        task_id = self._next_id
        self._next_id += 1

        task = Task(
            id=task_id,
            title=title.strip(),
            description=description.strip() if description else "",
            completed=False
        )

        # Validate task before storing
        task.validate()

        # Store the task
        self._tasks[task_id] = task

        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the todo list.

        Returns:
            List[Task]: List of all Task objects, sorted by ID
        """
        return sorted(list(self._tasks.values()), key=lambda x: x.id)

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a specific task by ID.

        Args:
            task_id (int): Unique identifier of the task

        Returns:
            Task: Task object matching the ID

        Raises:
            ValueError: If task with given ID does not exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        return self._tasks[task_id]

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Task:
        """
        Update an existing task's details.

        Args:
            task_id (int): Unique identifier of the task to update
            title (str, optional): New title (if provided)
            description (str, optional): New description (if provided)

        Returns:
            Task: Updated Task object

        Raises:
            ValueError: If task with given ID does not exist or new title is invalid
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]

        # Update title if provided
        if title is not None:
            # Validate new title if it's being changed
            if title != task.title:
                if not title or not title.strip():
                    raise ValueError("Task title must not be empty or contain only whitespace")
                task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description.strip() if description else ""

        # Re-validate the task after updates
        task.validate()

        return task

    def toggle_task_status(self, task_id: int) -> Task:
        """
        Toggle a task's completion status.

        Args:
            task_id (int): Unique identifier of the task

        Returns:
            Task: Task object with toggled completion status

        Raises:
            ValueError: If task with given ID does not exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]
        task.completed = not task.completed  # Toggle the status

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.

        Args:
            task_id (int): Unique identifier of the task to delete

        Returns:
            bool: True if task was successfully deleted, False otherwise

        Raises:
            ValueError: If task with given ID does not exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        del self._tasks[task_id]
        return True