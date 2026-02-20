from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager
from dapr.ext.fastapi import DaprApp
import logging
import asyncio
from typing import AsyncGenerator

from src.api.v1.endpoints import router
from src.config import settings
from src.database.database import engine
from src.models.task import Task
from src.models.user import User
from src.models.event import Event, Notification
from sqlmodel import SQLModel
from src.services.recurring_service import RecurringTaskService
from src.services.reminder_service import ReminderService
from src.database.database import get_session
from src.services.event_processor import EventProcessorService
from src.middleware.tracing import setup_tracing
from src.services.metrics_service import metrics_middleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Background task for recurring tasks
async def recurring_task_scheduler():
    """Background task to process recurring tasks periodically."""
    while True:
        try:
            # Wait for 5 minutes before next check
            await asyncio.sleep(300)  # 5 minutes

            # Process recurring tasks
            with next(get_session()) as session:
                RecurringTaskService.process_recurring_tasks(session)

        except Exception as e:
            logger.error(f"Error in recurring task scheduler: {e}")


# Background task for reminders
async def reminder_scheduler():
    """Background task to process reminders periodically."""
    while True:
        try:
            # Wait for 1 minute before next check
            await asyncio.sleep(60)  # 1 minute

            # Process reminders
            with next(get_session()) as session:
                ReminderService.check_and_send_reminders(session)

        except Exception as e:
            logger.error(f"Error in reminder scheduler: {e}")


# Background task for event processing
async def event_processor():
    """Background task to process Kafka events."""
    try:
        await EventProcessorService.start_event_consumers()
    except Exception as e:
        logger.error(f"Error in event processor: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events"""
    # Startup
    logger.info("Starting up FastAPI application with Dapr integration")

    # Set up distributed tracing
    setup_tracing(app)

    # Create database tables
    SQLModel.metadata.create_all(engine)

    # Start background tasks
    asyncio.create_task(recurring_task_scheduler())
    asyncio.create_task(reminder_scheduler())
    asyncio.create_task(event_processor())

    yield

    logger.info("Shutting down FastAPI application")


# Initialize FastAPI app with lifespan management
app = FastAPI(
    title="Advanced Todo Chatbot API",
    description="API for advanced todo chatbot with recurring tasks, due dates, and reminders",
    version="1.0.0",
    lifespan=lifespan
)

# Add metrics middleware first
app.middleware("http")(metrics_middleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Dapr extension
dapr_app = DaprApp(app)


# Include API v1 routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Root endpoint for health check"""
    return {"message": "Advanced Todo Chatbot API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.utcnow().isoformat()}


# Include the existing router from v1
from src.services.metrics_service import get_metrics
from fastapi.responses import Response
from src.health.dapr_health import get_dapr_health_status

@app.get("/metrics")
def get_prometheus_metrics():
    """Endpoint to expose Prometheus metrics."""
    return Response(content=get_metrics(), media_type="text/plain")

@app.get("/dapr/health")
async def dapr_health_check():
    """Endpoint to check Dapr sidecar health."""
    return await get_dapr_health_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)