from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from typing import Optional
from sqlmodel import Session
from src.database.database import get_session
from src.auth.middleware import get_current_user
from src.services.todo_service import TodoService
from src.models.todo_item import TodoItemCreate, TodoItemUpdate
from src.schemas.todo_item import (
    TodoItemCreate as TodoItemCreateSchema,
    TodoItemUpdate as TodoItemUpdateSchema,
    TodoItemRead,
    TodoItemUpdateStatus,
    TodoItemList,
    TodoItemFilter
)


router = APIRouter()


@router.post("/", response_model=TodoItemRead)
def create_todo(
    todo_item: TodoItemCreateSchema,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo item."""
    try:
        # Create todo item using the service
        created_todo = TodoService.create_todo_item(
            session=session,
            todo_item=TodoItemCreate(**todo_item.dict()),
            user_id=UUID(current_user["user_id"])
        )
        # Convert to response schema
        return TodoItemRead(
            id=created_todo.id,
            title=created_todo.title,
            description=created_todo.description,
            status=created_todo.status,
            priority=created_todo.priority,
            due_date=created_todo.due_date,
            user_id=created_todo.user_id,
            created_at=created_todo.created_at,
            updated_at=created_todo.updated_at,
            completed_at=created_todo.completed_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=TodoItemList)
def get_todos(
    current_user: dict = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, description="Filter by status (pending, in_progress, completed)"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high, urgent)"),
    title: Optional[str] = Query(None, description="Search in title (partial match)"),
    limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    sort: str = Query("created_at", description="Sort by field (created_at, due_date, priority, title)"),
    sort_direction: str = Query("desc", description="Sort direction (asc or desc)"),
    session: Session = Depends(get_session)
):
    """Get user's todo items with optional filtering."""
    todos = TodoService.get_todo_items(
        session=session,
        user_id=UUID(current_user["user_id"]),
        status=status_filter,
        priority=priority,
        title=title,
        limit=limit,
        offset=offset,
        sort=sort,
        sort_direction=sort_direction
    )

    # Convert to read schema
    todo_items = [
        TodoItemRead(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            priority=todo.priority,
            due_date=todo.due_date,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            completed_at=todo.completed_at
        ) for todo in todos
    ]

    # Get total count for pagination
    # For simplicity, we'll just return the current batch size as total
    # In a real implementation, you'd want to query the total separately
    return TodoItemList(
        items=todo_items,
        total=len(todo_items),
        offset=offset,
        limit=limit
    )


@router.get("/{todo_id}", response_model=TodoItemRead)
def get_todo(
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific todo item."""
    todo = TodoService.get_todo_item_by_id(
        session=session,
        todo_id=todo_id,
        user_id=UUID(current_user["user_id"])
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )
    return TodoItemRead(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        status=todo.status,
        priority=todo.priority,
        due_date=todo.due_date,
        user_id=todo.user_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        completed_at=todo.completed_at
    )


@router.put("/{todo_id}", response_model=TodoItemRead)
def update_todo(
    todo_id: UUID,
    todo_update: TodoItemUpdateSchema,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific todo item."""
    updated_todo = TodoService.update_todo_item(
        session=session,
        todo_id=todo_id,
        todo_update=TodoItemUpdate(**todo_update.dict(exclude_unset=True)),
        user_id=UUID(current_user["user_id"])
    )
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )
    return TodoItemRead(
        id=updated_todo.id,
        title=updated_todo.title,
        description=updated_todo.description,
        status=updated_todo.status,
        priority=updated_todo.priority,
        due_date=updated_todo.due_date,
        user_id=updated_todo.user_id,
        created_at=updated_todo.created_at,
        updated_at=updated_todo.updated_at,
        completed_at=updated_todo.completed_at
    )


@router.patch("/{todo_id}/status", response_model=TodoItemRead)
def update_todo_status(
    todo_id: UUID,
    status_update: TodoItemUpdateStatus,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update only the status of a todo item."""
    updated_todo = TodoService.update_todo_status(
        session=session,
        todo_id=todo_id,
        new_status=status_update.status,
        user_id=UUID(current_user["user_id"])
    )
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )
    return TodoItemRead(
        id=updated_todo.id,
        title=updated_todo.title,
        description=updated_todo.description,
        status=updated_todo.status,
        priority=updated_todo.priority,
        due_date=updated_todo.due_date,
        user_id=updated_todo.user_id,
        created_at=updated_todo.created_at,
        updated_at=updated_todo.updated_at,
        completed_at=updated_todo.completed_at
    )


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific todo item."""
    success = TodoService.delete_todo_item(
        session=session,
        todo_id=todo_id,
        user_id=UUID(current_user["user_id"])
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo item not found"
        )
    return {"message": "Todo deleted successfully"}