'''
Task model for the Todo Console App
'''
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a todo item with attributes: ID (unique identifier),
    Title (required string), Description (optional string),
    Completed (boolean status), CreatedAt (timestamp)
    This implements T012: Task creation with auto-generated ID and timestamp
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        """Initialize the created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def validate(self):
        """
        Validate the task attributes according to business rules.
        Raises ValueError if validation fails.
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title must not be empty or contain only whitespace")