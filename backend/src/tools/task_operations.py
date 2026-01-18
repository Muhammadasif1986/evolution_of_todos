"""MCP Tools for Todo Operations"""

import json
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate
from src.database import engine
from src.services.task_service import TaskService
import uuid


async def add_task(task_title: str, task_description: Optional[str], user_id: str, due_date: Optional[str] = None, due_time: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool to create a new todo task

    Args:
        task_title: The title of the task to create
        task_description: Optional description of the task
        user_id: The ID of the user creating the task
        due_date: Optional due date in YYYY-MM-DD format
        due_time: Optional due time in HH:MM format

    Returns:
        Dictionary with success status and task information
    """
    try:
        # Parse due_date and due_time if provided
        parsed_due_date = None
        parsed_due_time = None

        if due_date:
            try:
                from datetime import datetime
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                return {
                    "success": False,
                    "task_id": None,
                    "task_title": task_title,
                    "message": f"Invalid date format. Please use YYYY-MM-DD format. Got: {due_date}"
                }

        if due_time:
            try:
                parsed_due_time = datetime.strptime(due_time, "%H:%M").time()
            except ValueError:
                return {
                    "success": False,
                    "task_id": None,
                    "task_title": task_title,
                    "message": f"Invalid time format. Please use HH:MM format. Got: {due_time}"
                }

        # Create a new task using the service
        task_data = TaskCreate(
            title=task_title,
            description=task_description,
            completed=False,
            due_date=parsed_due_date,
            due_time=parsed_due_time
        )

        with Session(engine) as session:
            new_task = TaskService.create_task(session=session, task=task_data, user_id=uuid.UUID(user_id))

        return {
            "success": True,
            "task_id": str(new_task.id),
            "task_title": new_task.title,
            "due_date": str(new_task.due_date) if new_task.due_date else None,
            "due_time": str(new_task.due_time.strftime('%H:%M')) if new_task.due_time else None,
            "message": f"Successfully created task: {new_task.title}"
        }
    except Exception as e:
        return {
            "success": False,
            "task_id": None,
            "task_title": task_title,
            "message": f"Failed to create task: {str(e)}"
        }


async def list_tasks(user_id: str, filter_type: Optional[str] = "all") -> Dict[str, Any]:
    """
    MCP tool to list user's todo tasks

    Args:
        user_id: The ID of the user whose tasks to list
        filter_type: Filter type (all, completed, incomplete)

    Returns:
        Dictionary with success status and list of tasks
    """
    try:
        with Session(engine) as session:
            tasks = TaskService.get_tasks_by_user_id(session=session, user_id=uuid.UUID(user_id))

            # Apply filter if specified
            if filter_type == "completed":
                tasks = [t for t in tasks if t.completed]
            elif filter_type == "incomplete":
                tasks = [t for t in tasks if not t.completed]

            task_list = []
            for task in tasks:
                task_list.append({
                    "task_id": str(task.id),
                    "task_title": task.title,
                    "task_description": task.description,
                    "completed": task.completed,
                    "due_date": str(task.due_date) if task.due_date else None,
                    "due_time": str(task.due_time.strftime('%H:%M')) if task.due_time else None
                })

        return {
            "success": True,
            "tasks": task_list
        }
    except Exception as e:
        return {
            "success": False,
            "tasks": [],
            "message": f"Failed to list tasks: {str(e)}"
        }


async def complete_task(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    MCP tool to mark a task as completed

    Args:
        task_id: The ID of the task to complete
        user_id: The ID of the user requesting completion

    Returns:
        Dictionary with success status and confirmation
    """
    try:
        with Session(engine) as session:
            updated_task = TaskService.complete_task(
                session=session,
                task_id=int(task_id),
                user_id=uuid.UUID(user_id)
            )

            if updated_task:
                return {
                    "success": True,
                    "task_id": str(updated_task.id),
                    "message": f"Successfully completed task: {updated_task.title}"
                }
            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "message": "Task not found or user not authorized"
                }
    except Exception as e:
        return {
            "success": False,
            "task_id": task_id,
            "message": f"Failed to complete task: {str(e)}"
        }


async def delete_task(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    MCP tool to delete a task

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user requesting deletion

    Returns:
        Dictionary with success status and confirmation
    """
    try:
        with Session(engine) as session:
            deleted = TaskService.delete_task(
                session=session,
                task_id=int(task_id),
                user_id=uuid.UUID(user_id)
            )

            if deleted:
                return {
                    "success": True,
                    "task_id": task_id,
                    "message": f"Successfully deleted task with ID: {task_id}"
                }
            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "message": "Task not found or user not authorized"
                }
    except Exception as e:
        return {
            "success": False,
            "task_id": task_id,
            "message": f"Failed to delete task: {str(e)}"
        }


async def update_task(task_id: str, user_id: str, task_title: Optional[str] = None,
                     task_description: Optional[str] = None, due_date: Optional[str] = None,
                     due_time: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool to update a task

    Args:
        task_id: The ID of the task to update
        user_id: The ID of the user requesting update
        task_title: New title for the task (optional)
        task_description: New description for the task (optional)
        due_date: New due date in YYYY-MM-DD format (optional)
        due_time: New due time in HH:MM format (optional)

    Returns:
        Dictionary with success status and updated fields
    """
    try:
        from src.models.task import TaskUpdate

        # Parse due_date and due_time if provided
        parsed_due_date = None
        parsed_due_time = None

        if due_date is not None:  # Allow empty string to mean "set to null"
            if due_date.strip():  # Only parse if not empty
                try:
                    from datetime import datetime
                    parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    return {
                        "success": False,
                        "task_id": task_id,
                        "message": f"Invalid date format. Please use YYYY-MM-DD format. Got: {due_date}"
                    }
            else:  # Empty string means set to null
                parsed_due_date = None

        if due_time is not None:  # Allow empty string to mean "set to null"
            if due_time.strip():  # Only parse if not empty
                try:
                    parsed_due_time = datetime.strptime(due_time, "%H:%M").time()
                except ValueError:
                    return {
                        "success": False,
                        "task_id": task_id,
                        "message": f"Invalid time format. Please use HH:MM format. Got: {due_time}"
                    }
            else:  # Empty string means set to null
                parsed_due_time = None

        # Prepare update data
        update_data = {}
        if task_title is not None:
            update_data["title"] = task_title
        if task_description is not None:
            update_data["description"] = task_description
        if due_date is not None:
            update_data["due_date"] = parsed_due_date
        if due_time is not None:
            update_data["due_time"] = parsed_due_time

        if not update_data:
            return {
                "success": False,
                "task_id": task_id,
                "message": "No fields to update were provided"
            }

        # Create TaskUpdate object
        task_update = TaskUpdate(**update_data)

        with Session(engine) as session:
            updated_task = TaskService.update_task(
                session=session,
                task_id=int(task_id),
                task_update=task_update,
                user_id=uuid.UUID(user_id)
            )

            if updated_task:
                # Determine which fields were updated
                updated_fields = []
                if task_title is not None:
                    updated_fields.append('title')
                if task_description is not None:
                    updated_fields.append('description')
                if due_date is not None:
                    updated_fields.append('due_date')
                if due_time is not None:
                    updated_fields.append('due_time')

                return {
                    "success": True,
                    "task_id": str(updated_task.id),
                    "updated_fields": updated_fields,
                    "message": f"Successfully updated task: {updated_task.title}"
                }
            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "message": "Task not found or user not authorized"
                }
    except Exception as e:
        return {
            "success": False,
            "task_id": task_id,
            "message": f"Failed to update task: {str(e)}"
        }