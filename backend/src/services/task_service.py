from typing import List, Optional
from sqlmodel import Session, select, and_
from datetime import datetime
from src.models.task import Task, TaskCreate, TaskUpdate
from src.logging_config import get_logger
from uuid import UUID


logger = get_logger(__name__)


class TaskService:
    @staticmethod
    def create_task(session: Session, task: TaskCreate, user_id: UUID) -> Task:
        """Create a new task."""
        logger.info(f"Creating task for user {user_id}")
        db_task = Task(
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        logger.info(f"Task created with ID: {db_task.id}")
        return db_task

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: UUID) -> List[Task]:
        """Get all tasks for a specific user."""
        logger.info(f"Getting tasks for user {user_id}")
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user_id(session: Session, task_id: int, user_id: UUID) -> Optional[Task]:
        """Get a specific task by ID and user ID."""
        logger.info(f"Getting task {task_id} for user {user_id}")
        statement = select(Task).where(
            and_(Task.id == task_id, Task.user_id == user_id)
        )
        task = session.exec(statement).first()
        return task

    @staticmethod
    def update_task(session: Session, task_id: int, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
        """Update a specific task."""
        logger.info(f"Updating task {task_id} for user {user_id}")
        db_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if db_task:
            update_data = task_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_task, field, value)
            db_task.updated_at = datetime.utcnow()
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            logger.info(f"Task {task_id} updated")
        return db_task

    @staticmethod
    def complete_task(session: Session, task_id: int, user_id: UUID) -> Optional[Task]:
        """Mark a task as complete."""
        logger.info(f"Completing task {task_id} for user {user_id}")
        db_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if db_task:
            db_task.completed = True
            db_task.updated_at = datetime.utcnow()
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            logger.info(f"Task {task_id} marked as complete")
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: UUID) -> bool:
        """Delete a specific task."""
        logger.info(f"Deleting task {task_id} for user {user_id}")
        db_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if db_task:
            session.delete(db_task)
            session.commit()
            logger.info(f"Task {task_id} deleted")
            return True
        return False