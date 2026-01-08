from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database.database import get_session
from src.auth.middleware import get_current_user
from src.models.task import TaskCreate as TaskCreateModel, TaskUpdate as TaskUpdateModel, TaskRead as TaskReadModel
from src.schemas.task import TaskCreate, TaskUpdate, TaskRead
from src.services.task_service import TaskService
from uuid import UUID
from typing import List
from datetime import datetime


router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get authenticated user's tasks."""
    user_id = current_user["user_id"]

    # Get tasks using the service
    tasks = TaskService.get_tasks_by_user_id(session=session, user_id=user_id)

    # Convert to response schema
    return [TaskRead(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    ) for task in tasks]


@router.post("/tasks", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user."""
    user_id = current_user["user_id"]

    # Create task using the service
    created_task = TaskService.create_task(
        session=session,
        task=TaskCreateModel(**task.dict()),
        user_id=user_id
    )

    # Convert to response schema
    return TaskRead(
        id=created_task.id,
        user_id=created_task.user_id,
        title=created_task.title,
        description=created_task.description,
        completed=created_task.completed,
        created_at=created_task.created_at,
        updated_at=created_task.updated_at
    )


@router.get("/tasks/{id}", response_model=TaskRead)
def get_task(
    id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task for the authenticated user."""
    user_id = current_user["user_id"]

    # Get task using the service
    task = TaskService.get_task_by_id_and_user_id(session=session, task_id=id, user_id=user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Convert to response schema
    return TaskRead(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/tasks/{id}", response_model=TaskRead)
def update_task(
    id: int,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for the authenticated user."""
    user_id = current_user["user_id"]

    # Update task using the service
    updated_task = TaskService.update_task(
        session=session,
        task_id=id,
        task_update=TaskUpdateModel(**task_update.dict(exclude_unset=True)),
        user_id=user_id
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Convert to response schema
    return TaskRead(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.delete("/tasks/{id}")
def delete_task(
    id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for the authenticated user."""
    user_id = current_user["user_id"]

    # Delete task using the service
    success = TaskService.delete_task(session=session, task_id=id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully", "id": id}


@router.patch("/tasks/{id}/complete", response_model=TaskRead)
def complete_task(
    id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Mark a task as complete for the authenticated user."""
    user_id = current_user["user_id"]

    # Complete task using the service
    completed_task = TaskService.complete_task(session=session, task_id=id, user_id=user_id)
    if not completed_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Convert to response schema
    return TaskRead(
        id=completed_task.id,
        user_id=completed_task.user_id,
        title=completed_task.title,
        description=completed_task.description,
        completed=completed_task.completed,
        created_at=completed_task.created_at,
        updated_at=completed_task.updated_at
    )