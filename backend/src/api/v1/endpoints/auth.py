from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from uuid import UUID
from src.database.database import get_session
from src.auth.jwt import create_access_token
from src.auth.middleware import get_current_user
from src.services.user_service import UserService
from src.schemas.user import UserCreate, UserRead, Token, UserLogin
from src.utils.security import verify_password
from src.exceptions import InvalidCredentialsException, DuplicateEmailException


router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    try:
        created_user = UserService.create_user(session, user_create)
        return UserRead(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )
    except DuplicateEmailException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return JWT token."""
    user = UserService.authenticate_user(
        session,
        user_credentials.email,
        user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email, "username": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user():
    """Invalidate current session (client-side token removal)."""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserRead)
def get_current_user_info(current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get current user's information."""
    user_id = UUID(current_user["user_id"])
    user = UserService.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )