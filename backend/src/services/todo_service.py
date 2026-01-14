from typing import List, Optional
from sqlmodel import Session, select, and_, or_
from datetime import datetime
from uuid import UUID
from src.models.todo_item import TodoItem, TodoItemCreate, TodoItemUpdate, TodoStatus, TodoPriority
from src.exceptions import TodoNotFoundException
from src.logging_config import get_logger


logger = get_logger(__name__)


class TodoService:
    @staticmethod
    def create_todo_item(session: Session, todo_item: TodoItemCreate, user_id: UUID) -> TodoItem:
        """Create a new todo item."""
        logger.info(f"Creating todo item for user {user_id}")
        db_todo = TodoItem(
            title=todo_item.title,
            description=todo_item.description,
            status=todo_item.status,
            priority=todo_item.priority,
            due_date=todo_item.due_date,
            user_id=user_id
        )
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        logger.info(f"Todo item created with ID: {db_todo.id}")
        return db_todo

    @staticmethod
    def get_todo_item_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[TodoItem]:
        """Get a todo item by ID for a specific user."""
        logger.info(f"Retrieving todo item {todo_id} for user {user_id}")
        statement = select(TodoItem).where(
            and_(TodoItem.id == todo_id, TodoItem.user_id == user_id)
        )
        result = session.exec(statement).first()
        if result:
            logger.info(f"Todo item {todo_id} retrieved successfully")
        else:
            logger.info(f"Todo item {todo_id} not found for user {user_id}")
        return result

    @staticmethod
    def get_todo_items(
        session: Session,
        user_id: UUID,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        title: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        sort: str = "created_at",
        sort_direction: str = "desc"
    ) -> List[TodoItem]:
        """Get todo items for a specific user with optional filtering."""
        logger.info(f"Retrieving todo items for user {user_id} with filters - status: {status}, priority: {priority}, title: {title}, limit: {limit}, offset: {offset}, sort: {sort}, sort_direction: {sort_direction}")

        # Start with base query
        statement = select(TodoItem)

        # Apply filters
        from src.database.filters import apply_todo_filters
        statement = apply_todo_filters(
            statement,
            user_id=user_id,
            status=status,
            priority=priority,
            title=title
        )

        # Apply sorting
        from src.database.filters import apply_todo_sorting
        statement = apply_todo_sorting(
            statement,
            sort_field=sort,
            sort_direction=sort_direction
        )

        # Apply pagination
        statement = statement.offset(offset).limit(limit)
        logger.debug(f"Applied pagination - offset: {offset}, limit: {limit}")

        result = session.exec(statement).all()
        logger.info(f"Retrieved {len(result)} todo items for user {user_id}")
        return result

    @staticmethod
    def update_todo_item(
        session: Session,
        todo_id: UUID,
        todo_update: TodoItemUpdate,
        user_id: UUID
    ) -> Optional[TodoItem]:
        """Update a todo item."""
        logger.info(f"Updating todo item {todo_id} for user {user_id}")
        db_todo = TodoService.get_todo_item_by_id(session, todo_id, user_id)
        if not db_todo:
            logger.warning(f"Attempt to update non-existent todo item {todo_id} for user {user_id}")
            return None

        # Log the updates being applied
        update_fields = todo_update.dict(exclude_unset=True)
        logger.debug(f"Applying updates to todo item {todo_id}: {update_fields}")

        # Update fields that are provided
        for field, value in update_fields.items():
            if value is not None:
                old_value = getattr(db_todo, field)
                setattr(db_todo, field, value)
                logger.debug(f"Updated {field} from {old_value} to {value}")

        # If status is being updated to completed, set completed_at
        if todo_update.status == TodoStatus.COMPLETED and db_todo.status != TodoStatus.COMPLETED:
            db_todo.completed_at = datetime.utcnow()
            logger.info(f"Set completed_at for todo item {todo_id}")
        # If status is being updated from completed to something else, clear completed_at
        elif db_todo.status == TodoStatus.COMPLETED and todo_update.status != TodoStatus.COMPLETED:
            db_todo.completed_at = None
            logger.info(f"Cleared completed_at for todo item {todo_id}")

        db_todo.updated_at = datetime.utcnow()
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        logger.info(f"Todo item {todo_id} updated successfully")
        return db_todo

    @staticmethod
    def update_todo_status(
        session: Session,
        todo_id: UUID,
        new_status: TodoStatus,
        user_id: UUID
    ) -> Optional[TodoItem]:
        """Update only the status of a todo item."""
        logger.info(f"Updating status of todo item {todo_id} for user {user_id} to {new_status}")
        db_todo = TodoService.get_todo_item_by_id(session, todo_id, user_id)
        if not db_todo:
            logger.warning(f"Attempt to update status of non-existent todo item {todo_id} for user {user_id}")
            return None

        old_status = db_todo.status
        logger.info(f"Changing status of todo item {todo_id} from {old_status} to {new_status}")
        db_todo.status = new_status

        # Set completed_at if status is being updated to completed
        if new_status == TodoStatus.COMPLETED and old_status != TodoStatus.COMPLETED:
            db_todo.completed_at = datetime.utcnow()
            logger.info(f"Set completed_at for todo item {todo_id} (status changed to completed)")
        # Clear completed_at if status is being updated from completed to something else
        elif old_status == TodoStatus.COMPLETED and new_status != TodoStatus.COMPLETED:
            db_todo.completed_at = None
            logger.info(f"Cleared completed_at for todo item {todo_id} (status changed from completed)")

        db_todo.updated_at = datetime.utcnow()
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        logger.info(f"Status of todo item {todo_id} updated successfully")
        return db_todo

    @staticmethod
    def delete_todo_item(session: Session, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a todo item."""
        logger.info(f"Deleting todo item {todo_id} for user {user_id}")
        db_todo = TodoService.get_todo_item_by_id(session, todo_id, user_id)
        if not db_todo:
            logger.warning(f"Attempt to delete non-existent todo item {todo_id} for user {user_id}")
            return False

        session.delete(db_todo)
        session.commit()
        logger.info(f"Todo item {todo_id} deleted successfully")
        return True