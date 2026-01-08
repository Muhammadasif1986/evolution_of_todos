from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from src.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token with expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    # Use better_auth_secret if available, otherwise fallback to secret_key
    secret = settings.better_auth_secret if settings.better_auth_secret else settings.secret_key
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str):
    """Verify access token and return payload."""
    try:
        # Use better_auth_secret if available, otherwise fallback to secret_key
        secret = settings.better_auth_secret if settings.better_auth_secret else settings.secret_key
        payload = jwt.decode(token, secret, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )