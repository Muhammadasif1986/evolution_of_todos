from typing import Optional
from sqlmodel import Session, select
from uuid import UUID
from src.models.user import User, UserCreate, UserUpdate
from src.utils.security import get_password_hash, verify_password
from src.exceptions import UserNotFoundException, DuplicateEmailException
from src.logging_config import get_logger


logger = get_logger(__name__)


class UserService:
    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        logger.info(f"Creating user with email: {user_create.email}")

        # Check if user with email already exists
        existing_user = UserService.get_user_by_email(session, user_create.email)
        if existing_user:
            logger.warning(f"Attempt to create user with existing email: {user_create.email}")
            raise DuplicateEmailException()

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        logger.info(f"User created successfully with ID: {db_user.id}")
        return db_user

    @staticmethod
    def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        logger.info(f"Retrieving user with ID: {user_id}")
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if user:
            logger.info(f"User {user_id} retrieved successfully")
        else:
            logger.info(f"User {user_id} not found")

        return user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        logger.info(f"Retrieving user with email: {email}")
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if user:
            logger.info(f"User with email {email} retrieved successfully")
        else:
            logger.info(f"User with email {email} not found")

        return user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        logger.info(f"Authenticating user with email: {email}")
        user = UserService.get_user_by_email(session, email)

        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed for email: {email}")
            return None

        logger.info(f"User {email} authenticated successfully")
        return user

    @staticmethod
    def update_user(session: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        """Update a user."""
        logger.info(f"Updating user {user_id}")
        db_user = UserService.get_user_by_id(session, user_id)

        if not db_user:
            logger.warning(f"Attempt to update non-existent user {user_id}")
            return None

        # Check if email is being updated and if it already exists
        if user_update.email and user_update.email != db_user.email:
            existing_user = UserService.get_user_by_email(session, user_update.email)
            if existing_user:
                logger.warning(f"Attempt to update user {user_id} with existing email: {user_update.email}")
                raise DuplicateEmailException()

        # Update fields that are provided
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]  # Remove password from update data

        for field, value in update_data.items():
            if value is not None:
                setattr(db_user, field, value)

        db_user.updated_at = db_user.updated_at  # This will trigger the update
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        logger.info(f"User {user_id} updated successfully")
        return db_user

    @staticmethod
    def delete_user(session: Session, user_id: UUID) -> bool:
        """Delete a user."""
        logger.info(f"Deleting user {user_id}")
        db_user = UserService.get_user_by_id(session, user_id)

        if not db_user:
            logger.warning(f"Attempt to delete non-existent user {user_id}")
            return False

        session.delete(db_user)
        session.commit()

        logger.info(f"User {user_id} deleted successfully")
        return True