from prometheus_client import Counter, Histogram, Summary, Gauge, generate_latest
from fastapi import Request, Response
from typing import Dict, Any
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

TASK_OPERATIONS = Counter(
    'task_operations_total',
    'Total task operations',
    ['operation', 'status']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

TASK_PROCESSING_LATENCY = Histogram(
    'task_processing_duration_seconds',
    'Task processing latency'
)

def increment_request_count(method: str, endpoint: str, status: str):
    """Increment the request counter."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()

def record_request_latency(method: str, endpoint: str, latency: float):
    """Record request latency."""
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)

def increment_task_operation(operation: str, status: str = "success"):
    """Increment task operation counter."""
    TASK_OPERATIONS.labels(operation=operation, status=status).inc()

def set_active_users(count: int):
    """Set the number of active users."""
    ACTIVE_USERS.set(count)

def record_task_processing_latency(latency: float):
    """Record task processing latency."""
    TASK_PROCESSING_LATENCY.observe(latency)

async def metrics_middleware(request: Request, call_next):
    """Middleware to collect metrics."""
    start_time = time.time()

    response: Response = await call_next(request)

    # Record metrics
    latency = time.time() - start_time
    increment_request_count(
        method=request.method,
        endpoint=str(request.url.path),
        status=str(response.status_code)
    )
    record_request_latency(
        method=request.method,
        endpoint=str(request.url.path),
        latency=latency
    )

    return response

def get_metrics():
    """Get metrics in Prometheus format."""
    return generate_latest()

# Initialize some metrics
set_active_users(0)