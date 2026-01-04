from sqlmodel import select
from sqlalchemy import func
from src.models.todo_item import TodoItem, TodoStatus, TodoPriority
from typing import Optional
from uuid import UUID


def apply_todo_filters(
    query,
    user_id: UUID,
    status: Optional[TodoStatus] = None,
    priority: Optional[TodoPriority] = None,
    title: Optional[str] = None
):
    """
    Apply common filters to a TodoItem query.

    Args:
        query: The base query to apply filters to
        user_id: The user ID to filter todos for
        status: Optional status to filter by
        priority: Optional priority to filter by
        title: Optional title to filter by (contains search)

    Returns:
        Query with filters applied
    """
    # Always filter by user ID for security
    query = query.where(TodoItem.user_id == user_id)

    # Apply status filter
    if status:
        query = query.where(TodoItem.status == status)

    # Apply priority filter
    if priority:
        query = query.where(TodoItem.priority == priority)

    # Apply title search (case-insensitive partial match)
    if title:
        query = query.where(func.lower(TodoItem.title).contains(func.lower(title)))

    return query


def apply_todo_sorting(
    query,
    sort_field: str = "created_at",
    sort_direction: str = "desc"
):
    """
    Apply sorting to a TodoItem query.

    Args:
        query: The base query to apply sorting to
        sort_field: Field to sort by (created_at, due_date, priority, title)
        sort_direction: Direction to sort (asc or desc)

    Returns:
        Query with sorting applied
    """
    # Determine the column to sort by
    if sort_field == "created_at":
        sort_column = TodoItem.created_at
    elif sort_field == "due_date":
        sort_column = TodoItem.due_date
    elif sort_field == "priority":
        sort_column = TodoItem.priority
    elif sort_field == "title":
        sort_column = TodoItem.title
    else:
        # Default to created_at if invalid field
        sort_column = TodoItem.created_at

    # Apply sorting direction
    if sort_direction.lower() == "asc":
        query = query.order_by(sort_column)
    else:
        # Default to descending
        query = query.order_by(sort_column.desc())

    return query