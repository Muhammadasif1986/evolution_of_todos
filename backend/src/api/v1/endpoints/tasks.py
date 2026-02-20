from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, and_
from src.database.database import get_session
from src.auth.middleware import get_current_user
from src.models.task import Task as TaskModel
from src.schemas.task import TaskCreate, TaskUpdate, TaskRead
from src.services.task_service import TaskService
from uuid import UUID
from typing import List, Optional
from datetime import datetime, date
import json


router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    priority: Optional[str] = Query(None, description="Filter tasks by priority"),
    tag: Optional[str] = Query(None, description="Filter tasks by tag"),
    due_date_from: Optional[date] = Query(None, description="Filter tasks with due date from this date"),
    due_date_to: Optional[date] = Query(None, description="Filter tasks with due date to this date"),
    sort: Optional[str] = Query(None, description="Sort tasks by field and direction"),
    limit: int = Query(50, ge=1, le=100, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get authenticated user's tasks with filtering, sorting, and pagination."""
    user_id = current_user["user_id"]

    # Build query with filters
    statement = select(TaskModel).where(TaskModel.user_id == user_id)

    if status:
        statement = statement.where(TaskModel.status == status)
    if priority:
        statement = statement.where(TaskModel.priority == priority)
    if tag:
        # Filter by tag in tags array
        statement = statement.where(TaskModel.tags.contains([tag]))
    if due_date_from:
        statement = statement.where(TaskModel.due_date >= due_date_from)
    if due_date_to:
        statement = statement.where(TaskModel.due_date <= due_date_to)

    # Apply sorting
    if sort:
        field, direction = sort.split(':') if ':' in sort else (sort, 'asc')
        if hasattr(TaskModel, field):
            if direction.lower() == 'desc':
                statement = statement.order_by(getattr(TaskModel, field).desc())
            else:
                statement = statement.order_by(getattr(TaskModel, field).asc())

    # Apply pagination
    statement = statement.offset(offset).limit(limit)

    tasks = session.exec(statement).all()

    # Convert to response schema
    result_tasks = []
    for task in tasks:
        # Parse the JSON strings for recurrence pattern and reminder settings
        recurrence_pattern = None
        if task.recurrence_pattern:
            try:
                parsed_recurrence = json.loads(task.recurrence_pattern)
                from src.schemas.task import RecurrencePattern
                recurrence_pattern = RecurrencePattern(**parsed_recurrence)
            except:
                pass  # If parsing fails, set to None

        reminder_settings = None
        if task.reminder_settings:
            try:
                parsed_reminder = json.loads(task.reminder_settings)
                from src.schemas.task import ReminderSettings
                reminder_settings = ReminderSettings(**parsed_reminder)
            except:
                pass  # If parsing fails, set to None

        result_tasks.append(TaskRead(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            tags=task.tags,
            due_date=task.due_date,
            due_time=task.due_time,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            recurrence_pattern=recurrence_pattern,
            reminder_settings=reminder_settings
        ))

    return result_tasks


@router.post("/tasks", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user."""
    user_id = current_user["user_id"]

    from src.models.task import TaskCreate as TaskCreateModel
    # Create task using the service
    created_task = TaskService.create_task(
        session=session,
        task=TaskCreateModel(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            tags=task.tags,
            due_date=task.due_date,
            due_time=task.due_time,
            recurrence_pattern=task.recurrence_pattern,
            reminder_settings=task.reminder_settings,
        ),
        user_id=user_id
    )

    # Convert to response schema
    return TaskRead(
        id=created_task.id,
        user_id=created_task.user_id,
        title=created_task.title,
        description=created_task.description,
        status=created_task.status,
        priority=created_task.priority,
        tags=created_task.tags,
        due_date=created_task.due_date,
        due_time=created_task.due_time,
        created_at=created_task.created_at,
        updated_at=created_task.updated_at,
        completed_at=created_task.completed_at,
        recurrence_pattern=task.recurrence_pattern,  # Use original since model stores as JSON
        reminder_settings=task.reminder_settings    # Use original since model stores as JSON
    )


@router.get("/tasks/{id}", response_model=TaskRead)
def get_task(
    id: UUID,
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

    # Parse the JSON strings for recurrence pattern and reminder settings
    recurrence_pattern = None
    if task.recurrence_pattern:
        try:
            parsed_recurrence = json.loads(task.recurrence_pattern)
            from src.schemas.task import RecurrencePattern
            recurrence_pattern = RecurrencePattern(**parsed_recurrence)
        except:
            pass  # If parsing fails, set to None

    reminder_settings = None
    if task.reminder_settings:
        try:
            parsed_reminder = json.loads(task.reminder_settings)
            from src.schemas.task import ReminderSettings
            reminder_settings = ReminderSettings(**parsed_reminder)
        except:
            pass  # If parsing fails, set to None

    # Convert to response schema
    return TaskRead(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        tags=task.tags,
        due_date=task.due_date,
        due_time=task.due_time,
        created_at=task.created_at,
        updated_at=task.updated_at,
        completed_at=task.completed_at,
        recurrence_pattern=recurrence_pattern,
        reminder_settings=reminder_settings
    )


@router.put("/tasks/{id}", response_model=TaskRead)
def update_task(
    id: UUID,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for the authenticated user."""
    user_id = current_user["user_id"]

    from src.models.task import TaskUpdate as TaskUpdateModel
    # Update task using the service
    updated_task = TaskService.update_task(
        session=session,
        task_id=id,
        task_update=TaskUpdateModel(
            title=task_update.title,
            description=task_update.description,
            status=task_update.status,
            priority=task_update.priority,
            tags=task_update.tags,
            due_date=task_update.due_date,
            due_time=task_update.due_time,
            recurrence_pattern=task_update.recurrence_pattern,
            reminder_settings=task_update.reminder_settings,
        ),
        user_id=user_id
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Parse the JSON strings for recurrence pattern and reminder settings
    recurrence_pattern = None
    if updated_task.recurrence_pattern:
        try:
            parsed_recurrence = json.loads(updated_task.recurrence_pattern)
            from src.schemas.task import RecurrencePattern
            recurrence_pattern = RecurrencePattern(**parsed_recurrence)
        except:
            pass  # If parsing fails, set to None

    reminder_settings = None
    if updated_task.reminder_settings:
        try:
            parsed_reminder = json.loads(updated_task.reminder_settings)
            from src.schemas.task import ReminderSettings
            reminder_settings = ReminderSettings(**parsed_reminder)
        except:
            pass  # If parsing fails, set to None

    # Convert to response schema
    return TaskRead(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        status=updated_task.status,
        priority=updated_task.priority,
        tags=updated_task.tags,
        due_date=updated_task.due_date,
        due_time=updated_task.due_time,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at,
        completed_at=updated_task.completed_at,
        recurrence_pattern=recurrence_pattern,
        reminder_settings=reminder_settings
    )


@router.delete("/tasks/{id}")
def delete_task(
    id: UUID,
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


@router.post("/tasks/{id}/complete", response_model=TaskRead)
def complete_task(
    id: UUID,
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

    # Parse the JSON strings for recurrence pattern and reminder settings
    recurrence_pattern = None
    if completed_task.recurrence_pattern:
        try:
            parsed_recurrence = json.loads(completed_task.recurrence_pattern)
            from src.schemas.task import RecurrencePattern
            recurrence_pattern = RecurrencePattern(**parsed_recurrence)
        except:
            pass  # If parsing fails, set to None

    reminder_settings = None
    if completed_task.reminder_settings:
        try:
            parsed_reminder = json.loads(completed_task.reminder_settings)
            from src.schemas.task import ReminderSettings
            reminder_settings = ReminderSettings(**parsed_reminder)
        except:
            pass  # If parsing fails, set to None

    # Convert to response schema
    return TaskRead(
        id=completed_task.id,
        user_id=completed_task.user_id,
        title=completed_task.title,
        description=completed_task.description,
        status=completed_task.status,
        priority=completed_task.priority,
        tags=completed_task.tags,
        due_date=completed_task.due_date,
        due_time=completed_task.due_time,
        created_at=completed_task.created_at,
        updated_at=completed_task.updated_at,
        completed_at=completed_task.completed_at,
        recurrence_pattern=recurrence_pattern,
        reminder_settings=reminder_settings
    )


@router.get("/tasks/search", response_model=List[TaskRead])
def search_tasks(
    query: str = Query(..., description="Search query text"),
    limit: int = Query(50, ge=1, le=100, description="Limit number of results"),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Search tasks by text content."""
    user_id = current_user["user_id"]

    # Search tasks by title or description containing the query
    statement = select(TaskModel).where(
        and_(
            TaskModel.user_id == user_id,
            (TaskModel.title.contains(query) | TaskModel.description.contains(query))
        )
    ).limit(limit)

    tasks = session.exec(statement).all()

    # Convert to response schema
    result_tasks = []
    for task in tasks:
        # Parse the JSON strings for recurrence pattern and reminder settings
        recurrence_pattern = None
        if task.recurrence_pattern:
            try:
                parsed_recurrence = json.loads(task.recurrence_pattern)
                from src.schemas.task import RecurrencePattern
                recurrence_pattern = RecurrencePattern(**parsed_recurrence)
            except:
                pass  # If parsing fails, set to None

        reminder_settings = None
        if task.reminder_settings:
            try:
                parsed_reminder = json.loads(task.reminder_settings)
                from src.schemas.task import ReminderSettings
                reminder_settings = ReminderSettings(**parsed_reminder)
            except:
                pass  # If parsing fails, set to None

        result_tasks.append(TaskRead(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            tags=task.tags,
            due_date=task.due_date,
            due_time=task.due_time,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            recurrence_pattern=recurrence_pattern,
            reminder_settings=reminder_settings
        ))

    return result_tasks