from typing import Dict, Any, Optional
import json
from jsonschema import validate, ValidationError
from src.logging_config import get_logger


logger = get_logger(__name__)


# Define JSON schemas for different event types
TASK_EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {
            "type": "string",
            "enum": ["created", "updated", "completed", "deleted", "recurring-triggered"]
        },
        "task_id": {"type": ["string", "integer"]},
        "task_data": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "title": {"type": "string", "minLength": 1, "maxLength": 200},
                "description": {"type": ["string", "null"]},
                "status": {"type": "string", "enum": ["pending", "completed", "archived"]},
                "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "due_date": {"type": ["string", "null"]},
                "recurrence_pattern": {"type": ["object", "null"]},
                "created_at": {"type": "string"},
                "updated_at": {"type": "string"},
                "user_id": {"type": "string"}
            },
            "required": ["id", "title", "status", "priority", "created_at", "updated_at", "user_id"]
        },
        "user_id": {"type": "string"},
        "timestamp": {"type": "string"},
        "source": {"type": "string"}
    },
    "required": ["event_type", "task_id", "task_data", "user_id", "timestamp", "source"]
}


REMINDER_EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {"type": ["string", "integer"]},
        "title": {"type": "string"},
        "due_at": {"type": "string"},
        "remind_at": {"type": "string"},
        "user_id": {"type": "string"}
    },
    "required": ["task_id", "title", "due_at", "remind_at", "user_id"]
}


class EventValidationMiddleware:
    """Middleware to validate event schemas"""

    @staticmethod
    def validate_task_event(event_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate a task event against the schema."""
        try:
            validate(instance=event_data, schema=TASK_EVENT_SCHEMA)
            return True, None
        except ValidationError as e:
            error_msg = f"Task event validation error: {e.message} at {'.'.join(e.absolute_path)}"
            logger.error(error_msg)
            return False, error_msg

    @staticmethod
    def validate_reminder_event(event_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate a reminder event against the schema."""
        try:
            validate(instance=event_data, schema=REMINDER_EVENT_SCHEMA)
            return True, None
        except ValidationError as e:
            error_msg = f"Reminder event validation error: {e.message} at {'.'.join(e.absolute_path)}"
            logger.error(error_msg)
            return False, error_msg

    @staticmethod
    def validate_event(event_type: str, event_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate an event based on its type."""
        if event_type in ["created", "updated", "completed", "deleted", "recurring-triggered"]:
            return EventValidationMiddleware.validate_task_event(event_data)
        elif event_type == "reminder":
            return EventValidationMiddleware.validate_reminder_event(event_data)
        else:
            # For unknown event types, we might want to be flexible
            # or have a generic validation
            logger.warning(f"Unknown event type for validation: {event_type}")
            return True, None  # For now, allow unknown event types

    @staticmethod
    def sanitize_event_data(event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize event data to remove potentially harmful content."""
        # Deep copy the event data to avoid modifying the original
        sanitized = json.loads(json.dumps(event_data))

        # Remove any script tags or other potentially harmful content
        # This is a simplified sanitization - in production, use a proper sanitizer
        if "task_data" in sanitized and isinstance(sanitized["task_data"], dict):
            task_data = sanitized["task_data"]
            for key, value in task_data.items():
                if isinstance(value, str):
                    # Remove potential script tags
                    task_data[key] = value.replace("<script", "&lt;script").replace("javascript:", "javascript_")

        return sanitized


# Create a global instance for easy access
event_validator = EventValidationMiddleware()