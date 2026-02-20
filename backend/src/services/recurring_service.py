from datetime import datetime, timedelta, date
from typing import List, Optional
from sqlmodel import Session, select
from src.models.task import Task
from src.services.kafka_service import get_kafka_producer
from src.logging_config import get_logger
from uuid import UUID
import json
from src.models.recurrence_pattern import RecurrencePattern


logger = get_logger(__name__)


class RecurringTaskService:
    @staticmethod
    def process_recurring_tasks(session: Session):
        """Process recurring tasks and create new instances when needed."""
        logger.info("Processing recurring tasks...")

        # Get all recurring tasks
        statement = select(Task).where(Task.recurrence_pattern.is_not(None))
        recurring_tasks = session.exec(statement).all()

        for task in recurring_tasks:
            try:
                # Parse recurrence pattern
                if task.recurrence_pattern:
                    pattern_data = json.loads(task.recurrence_pattern)
                    recurrence = RecurrencePattern(**pattern_data)

                    # Check if this task should generate a new instance
                    if RecurringTaskService.should_generate_new_task(task, recurrence):
                        new_task = RecurringTaskService.create_next_instance(session, task, recurrence)
                        if new_task:
                            logger.info(f"Created new instance for recurring task {task.id}: {new_task.id}")

                            # Publish recurring task triggered event
                            try:
                                kafka_producer = get_kafka_producer()
                                task_data = {
                                    "id": str(new_task.id),
                                    "title": new_task.title,
                                    "description": new_task.description,
                                    "status": new_task.status,
                                    "priority": new_task.priority,
                                    "tags": new_task.tags,
                                    "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                                    "due_time": str(new_task.due_time) if new_task.due_time else None,
                                    "recurrence_pattern": new_task.recurrence_pattern,
                                    "user_id": str(new_task.user_id),
                                    "created_at": new_task.created_at.isoformat(),
                                    "updated_at": new_task.updated_at.isoformat(),
                                }
                                kafka_producer.publish_task_event(
                                    event_type="recurring-triggered",
                                    task_id=new_task.id,
                                    task_data=task_data,
                                    user_id=str(new_task.user_id)
                                )
                            except Exception as e:
                                logger.error(f"Failed to publish recurring task event: {e}")
            except Exception as e:
                logger.error(f"Error processing recurring task {task.id}: {e}")

    @staticmethod
    def should_generate_new_task(task: Task, recurrence: RecurrencePattern) -> bool:
        """Determine if a new task instance should be created based on recurrence pattern."""
        # Check if recurrence has ended
        if recurrence.end_date and date.today() > recurrence.end_date:
            return False

        # Check occurrence count
        if recurrence.occurrence_count:
            # Count how many tasks have been created from this pattern
            # This is a simplified check - in a real implementation you might track this differently
            pass

        # Check the recurrence type
        if recurrence.type == "daily":
            # Daily recurrence - create new task if the last one was completed today
            if task.completed_at and task.completed_at.date() == date.today():
                return True
        elif recurrence.type == "weekly":
            # Weekly recurrence
            if task.completed_at:
                next_weekly_date = task.completed_at.date() + timedelta(weeks=recurrence.interval)
                if next_weekly_date <= date.today():
                    # Check if it aligns with days of week if specified
                    if not recurrence.days_of_week or task.completed_at.strftime('%A').lower() in recurrence.days_of_week:
                        return True
        elif recurrence.type == "monthly":
            # Monthly recurrence
            if task.completed_at:
                # Add the month interval and check
                next_month = task.completed_at.month + recurrence.interval
                next_year = task.completed_at.year
                while next_month > 12:
                    next_month -= 12
                    next_year += 1

                next_date = task.completed_at.date().replace(year=next_year, month=next_month)
                if next_date <= date.today():
                    return True
        elif recurrence.type == "yearly":
            # Yearly recurrence
            if task.completed_at:
                next_year = task.completed_at.year + recurrence.interval
                next_date = task.completed_at.date().replace(year=next_year)
                if next_date <= date.today():
                    return True

        # This is a simplified implementation
        # In a real system, you'd want more sophisticated tracking of recurrence
        return False

    @staticmethod
    def create_next_instance(session: Session, original_task: Task, recurrence: RecurrencePattern) -> Optional[Task]:
        """Create a new instance of a recurring task."""
        # Create a new task based on the original
        new_task = Task(
            title=original_task.title,
            description=original_task.description,
            status="pending",
            priority=original_task.priority,
            tags=original_task.tags,
            due_date=original_task.due_date,  # Keep the same due date pattern
            due_time=original_task.due_time,
            recurrence_pattern=original_task.recurrence_pattern,
            reminder_settings=original_task.reminder_settings,
            user_id=original_task.user_id
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task

    @staticmethod
    def create_recurring_task_with_pattern(
        session: Session,
        task: Task,
        recurrence_pattern: RecurrencePattern
    ) -> Task:
        """Create a new recurring task with the specified pattern."""
        # Convert the recurrence pattern to JSON string for storage
        pattern_json = recurrence_pattern.model_dump_json()
        task.recurrence_pattern = pattern_json

        session.add(task)
        session.commit()
        session.refresh(task)

        return task