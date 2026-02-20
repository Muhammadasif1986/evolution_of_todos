import json
import asyncio
from typing import Dict, Any, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import logging
from datetime import datetime
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka topic names
TASK_EVENTS_TOPIC = "task-events"
REMINDERS_TOPIC = "reminders"
TASK_UPDATES_TOPIC = "task-updates"
DEAD_LETTER_TOPIC = "dead-letter-queue"


class TaskEventSchema(BaseModel):
    """Schema for task events following the defined specification"""
    event_type: str  # created, updated, completed, deleted, recurring-triggered
    task_id: int
    task_data: Dict[str, Any]  # Full task object
    user_id: str
    timestamp: datetime


class ReminderEventSchema(BaseModel):
    """Schema for reminder events following the defined specification"""
    task_id: int
    title: str
    due_at: datetime
    remind_at: datetime
    user_id: str


class KafkaProducerService:
    """Service for publishing events to Kafka topics"""

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self._connect()

    def _connect(self):
        """Create a Kafka producer connection"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                retries=3,
                linger_ms=5,
                batch_size=16384
            )
            logger.info("Connected to Kafka producer successfully")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka producer: {e}")
            raise

    def publish_task_event(self, event_type: str, task_id: int, task_data: dict, user_id: str, source: str = "backend"):
        """Publish a task-related event to the task-events topic"""
        try:
            event_data = {
                "event_type": event_type,
                "task_id": task_id,
                "task_data": task_data,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "source": source
            }

            future = self.producer.send(TASK_EVENTS_TOPIC, key=str(task_id), value=event_data)
            self.producer.flush()

            logger.info(f"Published {event_type} event for task {task_id} to {TASK_EVENTS_TOPIC}")
            return future
        except KafkaError as e:
            logger.error(f"Failed to publish task event: {e}")
            raise

    def publish_reminder_event(self, task_id: int, title: str, due_at: datetime, remind_at: datetime, user_id: str):
        """Publish a reminder event to the reminders topic"""
        try:
            event_data = {
                "task_id": task_id,
                "title": title,
                "due_at": due_at.isoformat(),
                "remind_at": remind_at.isoformat(),
                "user_id": user_id
            }

            future = self.producer.send(REMINDERS_TOPIC, key=str(task_id), value=event_data)
            self.producer.flush()

            logger.info(f"Published reminder event for task {task_id} to {REMINDERS_TOPIC}")
            return future
        except KafkaError as e:
            logger.error(f"Failed to publish reminder event: {e}")
            raise

    def publish_task_update(self, task_id: int, task_data: dict, user_id: str):
        """Publish a task update event to the task-updates topic"""
        try:
            event_data = {
                "task_id": task_id,
                "task_data": task_data,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }

            future = self.producer.send(TASK_UPDATES_TOPIC, key=str(task_id), value=event_data)
            self.producer.flush()

            logger.info(f"Published task update for task {task_id} to {TASK_UPDATES_TOPIC}")
            return future
        except KafkaError as e:
            logger.error(f"Failed to publish task update: {e}")
            raise

    def close(self):
        """Close the Kafka producer connection"""
        if self.producer:
            self.producer.close()


class KafkaConsumerService:
    """Service for consuming events from Kafka topics"""

    def __init__(self, bootstrap_servers: str = "localhost:9092", group_id: str = "todo-service"):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self._connect()

    def _connect(self):
        """Create a Kafka consumer connection"""
        try:
            self.consumer = KafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            logger.info("Connected to Kafka consumer successfully")
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka consumer: {e}")
            raise

    def consume_task_events(self):
        """Consume task events from the task-events topic"""
        self.consumer.subscribe([TASK_EVENTS_TOPIC])
        logger.info(f"Subscribed to {TASK_EVENTS_TOPIC}")

        for message in self.consumer:
            try:
                event_data = message.value
                logger.info(f"Received task event: {event_data['event_type']} for task {event_data['task_id']}")

                # Process the event based on its type
                yield event_data
            except Exception as e:
                logger.error(f"Error processing task event: {e}")

    def consume_reminder_events(self):
        """Consume reminder events from the reminders topic"""
        self.consumer.subscribe([REMINDERS_TOPIC])
        logger.info(f"Subscribed to {REMINDERS_TOPIC}")

        for message in self.consumer:
            try:
                event_data = message.value
                logger.info(f"Received reminder event for task {event_data['task_id']}")

                # Process the reminder event
                yield event_data
            except Exception as e:
                logger.error(f"Error processing reminder event: {e}")

    def consume_dead_letter_queue(self):
        """Consume messages from the dead letter queue for manual processing."""
        self.consumer.subscribe([DEAD_LETTER_TOPIC])
        logger.info(f"Subscribed to {DEAD_LETTER_TOPIC}")

        for message in self.consumer:
            try:
                event_data = message.value
                logger.info(f"Received message from dead letter queue: {event_data}")

                # Process the dead letter message (manual intervention might be needed)
                yield event_data
            except Exception as e:
                logger.error(f"Error processing dead letter message: {e}")

    def close(self):
        """Close the Kafka consumer connection"""
        if self.consumer:
            self.consumer.close()


# Global Kafka service instances
kafka_producer_service: Optional[KafkaProducerService] = None
kafka_consumer_service: Optional[KafkaConsumerService] = None


def get_kafka_producer() -> KafkaProducerService:
    """Get or create a Kafka producer service instance"""
    global kafka_producer_service
    if not kafka_producer_service:
        kafka_producer_service = KafkaProducerService()
    return kafka_producer_service


def get_kafka_consumer() -> KafkaConsumerService:
    """Get or create a Kafka consumer service instance"""
    global kafka_consumer_service
    if not kafka_consumer_service:
        kafka_consumer_service = KafkaConsumerService()
    return kafka_consumer_service