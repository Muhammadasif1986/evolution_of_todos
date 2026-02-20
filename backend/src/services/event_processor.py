import json
from typing import Dict, Any
from datetime import datetime
from sqlmodel import Session
from src.services.kafka_service import get_kafka_consumer, KafkaConsumerService, DEAD_LETTER_TOPIC
from src.models.event import Event
from src.logging_config import get_logger
from src.database.database import get_session
from uuid import UUID
import asyncio
from src.middleware.event_validation import event_validator


logger = get_logger(__name__)


class EventProcessorService:
    """Service for processing various types of events from Kafka with idempotency and error handling"""

    # In-memory set to track processed events for idempotency
    # In production, this would be in Redis or a database
    processed_events = set()

    @staticmethod
    def is_duplicate_event(event_data: Dict[str, Any]) -> bool:
        """Check if an event is a duplicate to ensure idempotency."""
        # Create a unique identifier for the event
        event_key = f"{event_data.get('event_type', 'unknown')}_{event_data.get('task_id', 'none')}_{event_data.get('timestamp', '')}"

        if event_key in EventProcessorService.processed_events:
            return True

        # Check in database if event with same ID already exists
        from sqlmodel import select
        with next(get_session()) as session:
            existing_event = session.exec(
                select(Event).where(
                    Event.event_type == event_data.get('event_type', 'unknown'),
                    Event.task_id == event_data.get('task_id'),
                    Event.timestamp == datetime.fromisoformat(event_data.get('timestamp', '')) if event_data.get('timestamp') else None
                )
            ).first()

            if existing_event:
                # Add to in-memory cache to avoid future DB queries
                EventProcessorService.processed_events.add(event_key)
                return True

        return False

    @staticmethod
    def process_task_event(event_data: Dict[str, Any], session: Session):
        """Process task-related events with idempotency and error handling."""
        try:
            # Validate the event data first
            is_valid, validation_error = event_validator.validate_event(
                event_data.get("event_type", "unknown"),
                event_data
            )

            if not is_valid:
                logger.error(f"Event validation failed: {validation_error}")

                # Send invalid event to dead letter queue
                try:
                    from src.services.kafka_service import get_kafka_producer
                    kafka_producer = get_kafka_producer()

                    dead_letter_data = {
                        "original_event": event_data,
                        "validation_error": validation_error,
                        "processed_at": datetime.utcnow().isoformat(),
                        "retry_count": 0
                    }

                    kafka_producer.producer.send(
                        DEAD_LETTER_TOPIC,
                        key=event_data.get("task_id", "unknown"),
                        value=dead_letter_data
                    )
                    kafka_producer.producer.flush()

                    logger.info(f"Invalid event sent to dead letter queue: {event_data.get('task_id')}")
                    return  # Don't process invalid events
                except Exception as dlq_error:
                    logger.error(f"Failed to send invalid event to dead letter queue: {dlq_error}")
                    return  # Don't process if we can't handle the invalid event properly

            # Sanitize the event data
            event_data = event_validator.sanitize_event_data(event_data)

            # Check for duplicate event
            if EventProcessorService.is_duplicate_event(event_data):
                logger.info(f"Duplicate event detected, skipping: {event_data.get('task_type', 'unknown')} for task {event_data.get('task_id')}")
                return

            event_type = event_data.get("event_type")
            task_id = event_data.get("task_id")
            user_id = event_data.get("user_id")
            timestamp = event_data.get("timestamp")

            logger.info(f"Processing {event_type} event for task {task_id}")

            # Create event record in the database
            db_event = Event(
                event_type=event_type,
                task_id=task_id,
                task_data=json.dumps(event_data.get("task_data", {})),
                user_id=user_id,
                source=event_data.get("source", "unknown"),
                timestamp=datetime.fromisoformat(timestamp) if timestamp and isinstance(timestamp, str) else datetime.utcnow()
            )
            session.add(db_event)
            session.commit()

            # Add to processed events cache
            event_key = f"{event_type}_{task_id}_{timestamp}"
            EventProcessorService.processed_events.add(event_key)

            # Handle specific event types
            if event_type == "recurring-triggered":
                logger.info(f"Recurring task triggered: {task_id}")
                # Handle recurring task processing here
                from src.services.recurring_service import RecurringTaskService
                # Additional logic can be added here

            elif event_type == "created":
                logger.info(f"Task created: {task_id}")
                # Schedule reminders for new tasks if needed
                from src.services.reminder_service import ReminderService
                from src.models.task import Task
                from sqlmodel import select
                task = session.exec(select(Task).where(Task.id == task_id)).first()
                if task and task.reminder_settings:
                    ReminderService.schedule_reminders_for_task(session, task)

            elif event_type in ["updated", "completed", "deleted"]:
                logger.info(f"Task {event_type}: {task_id}")
                # Handle other task events as needed

        except Exception as e:
            logger.error(f"Error processing task event: {e}")

            # Send failed event to dead letter queue
            try:
                from src.services.kafka_service import get_kafka_producer
                kafka_producer = get_kafka_producer()

                dead_letter_data = {
                    "original_event": event_data,
                    "error_message": str(e),
                    "processed_at": datetime.utcnow().isoformat(),
                    "retry_count": 0  # Add retry logic as needed
                }

                kafka_producer.producer.send(
                    DEAD_LETTER_TOPIC,
                    key=event_data.get("task_id", "unknown"),
                    value=dead_letter_data
                )
                kafka_producer.producer.flush()

                logger.info(f"Failed event sent to dead letter queue: {event_data.get('task_id')}")
            except Exception as dlq_error:
                logger.error(f"Failed to send event to dead letter queue: {dlq_error}")

            # Mark event as failed in DB if needed
            if "task_id" in event_data:
                db_event = Event(
                    event_type=event_data.get("event_type", "unknown"),
                    task_id=event_data.get("task_id"),
                    task_data=json.dumps(event_data),
                    user_id=event_data.get("user_id", ""),
                    source=event_data.get("source", "unknown"),
                    processed=False,
                    error_message=str(e)
                )
                session.add(db_event)
                session.commit()

    @staticmethod
    def process_reminder_event(event_data: Dict[str, Any], session: Session):
        """Process reminder-related events with idempotency and error handling."""
        try:
            # Validate the reminder event
            is_valid, validation_error = event_validator.validate_event("reminder", event_data)

            if not is_valid:
                logger.error(f"Reminder event validation failed: {validation_error}")

                # Send invalid event to dead letter queue
                try:
                    from src.services.kafka_service import get_kafka_producer
                    kafka_producer = get_kafka_producer()

                    dead_letter_data = {
                        "original_event": event_data,
                        "validation_error": validation_error,
                        "processed_at": datetime.utcnow().isoformat(),
                        "retry_count": 0
                    }

                    kafka_producer.producer.send(
                        DEAD_LETTER_TOPIC,
                        key=event_data.get("task_id", "unknown"),
                        value=dead_letter_data
                    )
                    kafka_producer.producer.flush()

                    logger.info(f"Invalid reminder event sent to dead letter queue: {event_data.get('task_id')}")
                    return  # Don't process invalid events
                except Exception as dlq_error:
                    logger.error(f"Failed to send invalid reminder event to dead letter queue: {dlq_error}")
                    return  # Don't process if we can't handle the invalid event properly

            # Sanitize the event data
            event_data = event_validator.sanitize_event_data(event_data)

            # Create a simple event key for idempotency check (using timestamp and task_id)
            event_key = f"reminder_{event_data.get('task_id', 'none')}_{event_data.get('remind_at', '')}"

            # In a real application, we would check this more thoroughly
            # For now, just process the event
            task_id = event_data.get("task_id")
            user_id = event_data.get("user_id", "")
            title = event_data.get("title", "")

            # Parse the datetime strings
            due_at = datetime.fromisoformat(event_data["due_at"]) if "due_at" in event_data else None
            remind_at = datetime.fromisoformat(event_data["remind_at"]) if "remind_at" in event_data else None

            logger.info(f"Processing reminder event for task {task_id}")

            # Create notification record
            from src.models.event import Notification
            notification = Notification(
                task_id=task_id,
                title=title,
                due_at=due_at,
                remind_at=remind_at,
                user_id=user_id,
                notification_type=event_data.get("notification_type", "email"),
                status="pending"
            )
            session.add(notification)
            session.commit()

            # Additional processing can be added here, such as sending the actual notification
            logger.info(f"Reminder scheduled for task {task_id}")

        except Exception as e:
            logger.error(f"Error processing reminder event: {e}")

            # Send failed event to dead letter queue
            try:
                from src.services.kafka_service import get_kafka_producer
                kafka_producer = get_kafka_producer()

                dead_letter_data = {
                    "original_event": event_data,
                    "error_message": str(e),
                    "processed_at": datetime.utcnow().isoformat(),
                    "retry_count": 0
                }

                kafka_producer.producer.send(
                    DEAD_LETTER_TOPIC,
                    key=event_data.get("task_id", "unknown"),
                    value=dead_letter_data
                )
                kafka_producer.producer.flush()

                logger.info(f"Failed reminder event sent to dead letter queue: {event_data.get('task_id')}")
            except Exception as dlq_error:
                logger.error(f"Failed to send reminder event to dead letter queue: {dlq_error}")

    @staticmethod
    async def start_event_consumers():
        """Start Kafka consumers for all event types."""
        logger.info("Starting Kafka event consumers...")

        consumer_service = get_kafka_consumer()

        # Process events in the background
        while True:
            try:
                # Process task events
                for task_event in consumer_service.consume_task_events():
                    with next(get_session()) as session:
                        EventProcessorService.process_task_event(task_event, session)
                        # Small delay to prevent overwhelming the system
                        await asyncio.sleep(0.01)

                # Process reminder events
                for reminder_event in consumer_service.consume_reminder_events():
                    with next(get_session()) as session:
                        EventProcessorService.process_reminder_event(reminder_event, session)
                        # Small delay to prevent overwhelming the system
                        await asyncio.sleep(0.01)

            except Exception as e:
                logger.error(f"Error in event consumers: {e}")
                # Wait for a bit before retrying
                await asyncio.sleep(10)