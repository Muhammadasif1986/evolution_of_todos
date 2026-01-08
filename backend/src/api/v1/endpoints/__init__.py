from fastapi import APIRouter

# Create main API router
router = APIRouter()

# Import and include all endpoint routers
from . import todos, auth, tasks

# Include routers with prefixes
router.include_router(todos.router, prefix="/todos", tags=["todos"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(tasks.router, tags=["tasks"])