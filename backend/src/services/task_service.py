from typing import List, Optional
import json
from sqlmodel import Session, select, and_
from datetime import datetime, timezone
from src.models.task import Task, TaskCreate as TaskCreateModel, TaskUpdate as TaskUpdateModel
from src.logging_config import get_logger
from uuid import UUID
from src.services.kafka_service import get_kafka_producer
from src.models.recurrence_pattern import RecurrencePattern
from src.models.reminder_settings import ReminderSettings


logger = get_logger(__name__)


class TaskService:
    @staticmethod
    def create_task(session: Session, task: TaskCreateModel, user_id: UUID) -> Task:
        """Create a new task with support for recurring tasks and reminders."""
        logger.info(f"Creating task for user {user_id}")

        # Convert recurrence pattern and reminder settings to JSON
        recurrence_pattern_json = None
        if task.recurrence_pattern:
            recurrence_pattern_json = task.recurrence_pattern.model_dump_json()

        reminder_settings_json = None
        if task.reminder_settings:
            reminder_settings_json = task.reminder_settings.model_dump_json()

        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            tags=task.tags,
            due_date=task.due_date,
            due_time=task.due_time,
            recurrence_pattern=recurrence_pattern_json,
            reminder_settings=reminder_settings_json,
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        logger.info(f"Task created with ID: {db_task.id}")

        # Publish task created event
        try:
            kafka_producer = get_kafka_producer()
            task_data = {
                "id": str(db_task.id),
                "title": db_task.title,
                "description": db_task.description,
                "status": db_task.status,
                "priority": db_task.priority,
                "tags": db_task.tags,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "due_time": str(db_task.due_time) if db_task.due_time else None,
                "recurrence_pattern": db_task.recurrence_pattern,
                "user_id": str(db_task.user_id),
                "created_at": db_task.created_at.isoformat(),
                "updated_at": db_task.updated_at.isoformat(),
            }
            kafka_producer.publish_task_event(
                event_type="created",
                task_id=db_task.id,
                task_data=task_data,
                user_id=str(user_id)
            )
        except Exception as e:
            logger.error(f"Failed to publish task creation event: {e}")

        return db_task

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: UUID) -> List[Task]:
        """Get all tasks for a specific user."""
        logger.info(f"Getting tasks for user {user_id}")
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Get a specific task by ID and user ID."""
        logger.info(f"Getting task {task_id} for user {user_id}")
        statement = select(Task).where(
            and_(Task.id == task_id, Task.user_id == user_id)
        )
        task = session.exec(statement).first()
        return task

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_update: TaskUpdateModel, user_id: UUID) -> Optional[Task]:
        """Update a specific task with support for recurring tasks and reminders."""
        logger.info(f"Updating task {task_id} for user {user_id}")
        db_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if db_task:
            # Update the fields from task_update
            update_data = task_update.model_dump(exclude_unset=True)

            # Handle special fields like recurrence_pattern and reminder_settings
            if 'recurrence_pattern' in update_data and update_data['recurrence_pattern']:
                update_data['recurrence_pattern'] = update_data['recurrence_pattern'].model_dump_json()
            elif 'recurrence_pattern' in update_data and update_data['recurrence_pattern'] is None:
                update_data['recurrence_pattern'] = None

            if 'reminder_settings' in update_data and update_data['reminder_settings']:
                update_data['reminder_settings'] = update_data['reminder_settings'].model_dump_json()
            elif 'reminder_settings' in update_data and update_data['reminder_settings'] is None:
                update_data['reminder_settings'] = None

            for field, value in update_data.items():
                if value is not None:
                    setattr(db_task, field, value)

            db_task.updated_at = datetime.now(timezone.utc)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            logger.info(f"Task {task_id} updated")

            # Publish task updated event
            try:
                kafka_producer = get_kafka_producer()
                task_data = {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "status": db_task.status,
                    "priority": db_task.priority,
                    "tags": db_task.tags,
                    "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                    "due_time": str(db_task.due_time) if db_task.due_time else None,
                    "recurrence_pattern": db_task.recurrence_pattern,
                    "user_id": str(db_task.user_id),
                    "created_at": db_task.created_at.isoformat(),
                    "updated_at": db_task.updated_at.isoformat(),
                }
                kafka_producer.publish_task_event(
                    event_type="updated",
                    task_id=db_task.id,
                    task_data=task_data,
                    user_id=str(user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish task update event: {e}")

        return db_task

    @staticmethod
    def complete_task(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Mark a task as complete."""
        logger.info(f"Completing task {task_id} for user {user_id}")
        db_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if db_task:
            db_task.status = "completed"
            db_task.completed_at = datetime.now(timezone.utc)
            db_task.updated_at = datetime.now(timezone.utc)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            logger.info(f"Task {task_id} marked as complete")

            # Publish task completed event
            try:
                kafka_producer = get_kafka_producer()
                task_data = {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "status": db_task.status,
                    "priority": db_task.priority,
                    "tags": db_task.tags,
                    "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                    "due_time": str(db_task.due_time) if db_task.due_time else None,
                    "recurrence_pattern": db_task.recurrence_pattern,
                    "user_id": str(db_task.user_id),
                    "created_at": db_task.created_at.isoformat(),
                    "updated_at": db_task.updated_at.isoformat(),
                    "completed_at": db_task.completed_at.isoformat() if db_task.completed_at else None
                }
                kafka_producer.publish_task_event(
                    event_type="completed",
                    task_id=db_task.id,
                    task_data=task_data,
                    user_id=str(user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish task completion event: {e}")

        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
        """Delete a specific task."""
        logger.info(f"Deleting task {task_id} for user {user_id}")
        db_task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if db_task:
            session.delete(db_task)
            session.commit()
            logger.info(f"Task {task_id} deleted")

            # Publish task deleted event
            try:
                kafka_producer = get_kafka_producer()
                kafka_producer.publish_task_event(
                    event_type="deleted",
                    task_id=db_task.id,
                    task_data={},  # Empty as the task is deleted
                    user_id=str(user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish task deletion event: {e}")

            return True
        return False