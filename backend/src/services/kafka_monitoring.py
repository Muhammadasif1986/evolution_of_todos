from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Any
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Kafka-specific metrics
KAFKA_EVENT_PROCESSED = Counter(
    'kafka_events_processed_total',
    'Total Kafka events processed',
    ['event_type', 'topic', 'status']
)

KAFKA_EVENT_PROCESSING_LATENCY = Histogram(
    'kafka_event_processing_duration_seconds',
    'Kafka event processing latency',
    ['event_type', 'topic']
)

KAFKA_CONSUMER_LAG = Gauge(
    'kafka_consumer_lag',
    'Kafka consumer lag',
    ['topic', 'partition']
)

KAFKA_EVENT_QUEUE_SIZE = Gauge(
    'kafka_event_queue_size',
    'Current size of event processing queue',
    ['topic']
)

KAFKA_PROCESSING_SUCCESS_RATE = Gauge(
    'kafka_processing_success_rate',
    'Success rate of Kafka event processing',
    ['topic']
)

EVENT_PROCESSING_ERRORS = Counter(
    'event_processing_errors_total',
    'Total errors during event processing',
    ['error_type', 'event_type']
)


class KafkaMonitoringService:
    """Service for monitoring Kafka event processing with reliability metrics"""

    def __init__(self):
        self.event_counts = {}
        self.error_counts = {}
        self.start_times = {}
        self.success_counts = {}
        self.failure_counts = {}

    def record_event_received(self, event_type: str, topic: str):
        """Record that an event was received from Kafka."""
        key = f"{topic}:{event_type}"
        self.start_times[key] = time.time()

        # Update queue size gauge
        current_size = self.event_counts.get(key, 0)
        self.event_counts[key] = current_size + 1
        KAFKA_EVENT_QUEUE_SIZE.labels(topic=topic).set(self.event_counts[key])

    def record_event_processed(self, event_type: str, topic: str, success: bool = True):
        """Record that an event was processed."""
        key = f"{topic}:{event_type}"

        # Calculate and record processing latency
        start_time = self.start_times.pop(key, time.time())
        latency = time.time() - start_time
        KAFKA_EVENT_PROCESSING_LATENCY.labels(event_type=event_type, topic=topic).observe(latency)

        # Record processing result
        status = "success" if success else "failure"
        KAFKA_EVENT_PROCESSED.labels(event_type=event_type, topic=topic, status=status).inc()

        # Update success/failure counts
        if success:
            self.success_counts[key] = self.success_counts.get(key, 0) + 1
        else:
            self.failure_counts[key] = self.failure_counts.get(key, 0) + 1

        # Calculate and update success rate
        total = self.success_counts.get(key, 0) + self.failure_counts.get(key, 0)
        if total > 0:
            success_rate = self.success_counts.get(key, 0) / total
            KAFKA_PROCESSING_SUCCESS_RATE.labels(topic=topic).set(success_rate)

        # Update queue size
        current_size = self.event_counts.get(key, 1)
        self.event_counts[key] = max(0, current_size - 1)
        KAFKA_EVENT_QUEUE_SIZE.labels(topic=topic).set(self.event_counts[key])

    def record_processing_error(self, event_type: str, error_type: str = "unknown"):
        """Record a processing error."""
        EVENT_PROCESSING_ERRORS.labels(error_type=error_type, event_type=event_type).inc()

    def record_consumer_lag(self, topic: str, partition: int, lag: int):
        """Record consumer lag for monitoring."""
        KAFKA_CONSUMER_LAG.labels(topic=topic, partition=str(partition)).set(lag)

    def get_reliability_metrics(self, topic: str) -> Dict[str, Any]:
        """Get reliability metrics for a specific topic."""
        success_count = sum(v for k, v in self.success_counts.items() if k.startswith(topic))
        failure_count = sum(v for k, v in self.failure_counts.items() if k.startswith(topic))
        total = success_count + failure_count

        reliability_rate = (success_count / total * 100) if total > 0 else 100.0

        return {
            "topic": topic,
            "total_processed": total,
            "success_count": success_count,
            "failure_count": failure_count,
            "reliability_rate": reliability_rate,
            "target_reliability": 99.0,  # 99% target
            "reliability_target_met": reliability_rate >= 99.0
        }

    def get_all_reliability_metrics(self) -> Dict[str, Any]:
        """Get reliability metrics for all topics."""
        topics = set(k.split(':')[0] for k in list(self.success_counts.keys()) + list(self.failure_counts.keys()))
        metrics = {}

        for topic in topics:
            metrics[topic] = self.get_reliability_metrics(topic)

        # Overall metrics
        all_success = sum(self.success_counts.values())
        all_failure = sum(self.failure_counts.values())
        all_total = all_success + all_failure

        overall_reliability = (all_success / all_total * 100) if all_total > 0 else 100.0

        return {
            "overall": {
                "total_processed": all_total,
                "success_count": all_success,
                "failure_count": all_failure,
                "reliability_rate": overall_reliability,
                "target_reliability": 99.0,
                "reliability_target_met": overall_reliability >= 99.0
            },
            "by_topic": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }


# Global instance
kafka_monitor = KafkaMonitoringService()