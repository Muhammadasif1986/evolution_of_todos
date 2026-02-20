from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from src.models.task import Task
from src.models.event import Notification
from src.services.kafka_service import get_kafka_producer
from src.logging_config import get_logger
from uuid import UUID
import json
from src.models.reminder_settings import ReminderSettings


logger = get_logger(__name__)


class ReminderService:
    @staticmethod
    def schedule_reminders_for_task(session: Session, task: Task):
        """Schedule reminders for a task based on its reminder settings."""
        if not task.reminder_settings:
            return

        try:
            # Parse reminder settings
            settings_data = json.loads(task.reminder_settings)
            settings = ReminderSettings(**settings_data)

            if not settings.enabled:
                return

            # Calculate reminder time
            if task.due_date and task.due_time:
                due_datetime = datetime.combine(task.due_date, task.due_time)
                remind_datetime = due_datetime - timedelta(minutes=settings.time_before)
            elif task.due_date:
                due_datetime = datetime.combine(task.due_date, datetime.min.time())
                remind_datetime = due_datetime - timedelta(minutes=settings.time_before)
            else:
                return  # No due date, can't schedule reminder

            # Create notification record
            notification = Notification(
                task_id=task.id,
                title=f"Reminder: {task.title}",
                due_at=due_datetime,
                remind_at=remind_datetime,
                user_id=str(task.user_id),
                notification_type=settings.notification_channels[0] if settings.notification_channels else "email",
                status="pending"
            )

            session.add(notification)
            session.commit()
            session.refresh(notification)

            # Publish reminder event to Kafka
            try:
                kafka_producer = get_kafka_producer()
                kafka_producer.publish_reminder_event(
                    task_id=task.id,
                    title=notification.title,
                    due_at=due_datetime,
                    remind_at=remind_datetime,
                    user_id=str(task.user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish reminder event: {e}")

            logger.info(f"Reminder scheduled for task {task.id} at {remind_datetime}")
        except Exception as e:
            logger.error(f"Error scheduling reminder for task {task.id}: {e}")

    @staticmethod
    def check_and_send_reminders(session: Session):
        """Check for pending reminders and mark them as ready to send."""
        logger.info("Checking for pending reminders...")

        # Get all notifications that should be sent now
        statement = select(Notification).where(
            (Notification.status == "pending") &
            (Notification.remind_at <= datetime.now())
        )
        notifications = session.exec(statement).all()

        for notification in notifications:
            logger.info(f"Reminder ready for task {notification.task_id}, user {notification.user_id}")
            # In a real system, this would trigger the actual notification delivery
            # For now, we just log it and update the status
            notification.status = "ready"
            session.add(notification)

        session.commit()

    @staticmethod
    def schedule_reminders_for_all_tasks(session: Session):
        """Schedule reminders for all tasks that have reminder settings."""
        logger.info("Scheduling reminders for all tasks...")

        # Get all tasks with reminder settings
        statement = select(Task).where(Task.reminder_settings.is_not(None))
        tasks = session.exec(statement).all()

        for task in tasks:
            ReminderService.schedule_reminders_for_task(session, task)

    @staticmethod
    def get_upcoming_reminders(session: Session, user_id: UUID, hours_ahead: int = 24) -> List[Notification]:
        """Get upcoming reminders for a user within the specified hours."""
        cutoff_time = datetime.now() + timedelta(hours=hours_ahead)

        statement = select(Notification).where(
            (Notification.user_id == str(user_id)) &
            (Notification.remind_at <= cutoff_time) &
            (Notification.status.in_(["pending", "ready"]))
        ).order_by(Notification.remind_at.asc())

        return session.exec(statement).all()