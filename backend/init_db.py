from src.database.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.todo_item import TodoItem
from src.models.todo_chat_models import Conversation, Message
from sqlmodel import SQLModel

def init_db():
    """Initialize the database by dropping and recreating all tables."""
    print("Dropping database tables...")
    SQLModel.metadata.drop_all(bind=engine)
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()