import json
from datetime import datetime
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from src.models.event import Event
from src.logging_config import get_logger
from src.database.database import get_session
from src.services.kafka_service import get_kafka_consumer, KafkaConsumerService
import asyncio


logger = get_logger(__name__)


class AuditLog:
    """Model for audit logs"""

    def __init__(self, user_id: str, action: str, resource_type: str, resource_id: str,
                 old_values: Optional[Dict] = None, new_values: Optional[Dict] = None,
                 ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        self.timestamp = datetime.utcnow()
        self.user_id = user_id
        self.action = action  # create, update, delete, read
        self.resource_type = resource_type  # task, user, etc.
        self.resource_id = resource_id
        self.old_values = old_values or {}
        self.new_values = new_values or {}
        self.ip_address = ip_address
        self.user_agent = user_agent


class AuditService:
    """Service for audit logging that consumes task events"""

    @staticmethod
    def log_event(event_data: Dict[str, Any], session: Session):
        """Log an event to the audit trail."""
        try:
            event_type = event_data.get("event_type", "unknown")
            task_id = event_data.get("task_id")
            user_id = event_data.get("user_id", "system")
            source = event_data.get("source", "unknown")
            task_data = event_data.get("task_data", {})

            # Map event types to audit actions
            action_map = {
                "created": "create",
                "updated": "update",
                "completed": "update",
                "deleted": "delete",
                "recurring-triggered": "create",
                "reminder-scheduled": "create"
            }

            action = action_map.get(event_type, "unknown")

            # Create audit log entry
            audit_entry = Event(
                event_type=f"audit_{event_type}",
                task_id=task_id,
                task_data=json.dumps({
                    "action": action,
                    "resource_type": "task",
                    "old_values": {},
                    "new_values": task_data,
                    "ip_address": "system",
                    "user_agent": "event_processor",
                    "source": source
                }),
                user_id=user_id,
                source="audit_service",
                timestamp=datetime.utcnow()
            )

            session.add(audit_entry)
            session.commit()

            logger.info(f"Audit log created for {action} of task {task_id} by user {user_id}")

        except Exception as e:
            logger.error(f"Error creating audit log: {e}")

    @staticmethod
    def get_audit_trail(user_id: str, resource_type: str = None,
                        start_date: datetime = None, end_date: datetime = None,
                        session: Session = None) -> list:
        """Retrieve audit trail for a user or resource."""
        try:
            statement = select(Event).where(
                Event.event_type.like("audit_%"),
                Event.user_id == user_id
            )

            if resource_type:
                # Filter by resource type if specified
                pass  # This would be more complex in a real implementation

            if start_date:
                statement = statement.where(Event.timestamp >= start_date)

            if end_date:
                statement = statement.where(Event.timestamp <= end_date)

            statement = statement.order_by(Event.timestamp.desc())

            audit_logs = session.exec(statement).all()
            return audit_logs

        except Exception as e:
            logger.error(f"Error retrieving audit trail: {e}")
            return []

    @staticmethod
    async def start_audit_consumer():
        """Start consuming task events for audit logging."""
        logger.info("Starting audit event consumer...")

        consumer_service = get_kafka_consumer()

        # Process task events for auditing
        while True:
            try:
                # Process task events for audit logging
                for task_event in consumer_service.consume_task_events():
                    with next(get_session()) as session:
                        AuditService.log_event(task_event, session)
                        # Small delay to prevent overwhelming the system
                        await asyncio.sleep(0.01)

            except Exception as e:
                logger.error(f"Error in audit consumer: {e}")
                # Wait for a bit before retrying
                await asyncio.sleep(10)

    @staticmethod
    def get_user_activity_summary(user_id: str, days: int = 7) -> Dict[str, Any]:
        """Get a summary of user activity for the specified number of days."""
        try:
            from datetime import timedelta
            start_date = datetime.utcnow() - timedelta(days=days)

            with next(get_session()) as session:
                statement = select(Event).where(
                    Event.event_type.like("audit_%"),
                    Event.user_id == user_id,
                    Event.timestamp >= start_date
                )

                audit_logs = session.exec(statement).all()

                # Count different types of actions
                action_counts = {}
                for log in audit_logs:
                    # Extract action from task_data
                    try:
                        task_data = json.loads(log.task_data)
                        action = task_data.get("action", "unknown")
                        action_counts[action] = action_counts.get(action, 0) + 1
                    except:
                        continue

                return {
                    "user_id": user_id,
                    "days": days,
                    "total_events": len(audit_logs),
                    "action_counts": action_counts,
                    "last_activity": max([log.timestamp for log in audit_logs]) if audit_logs else None
                }

        except Exception as e:
            logger.error(f"Error getting user activity summary: {e}")
            return {"error": str(e)}