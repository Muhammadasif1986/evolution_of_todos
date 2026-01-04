from pydantic import BaseModel
from typing import Optional, Any, Dict


class BaseResponse(BaseModel):
    """Base response model for all API responses."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = "healthy"
    timestamp: str
    version: str = "1.0.0"