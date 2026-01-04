from src.database.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.todo_item import TodoItem
from sqlmodel import SQLModel

def init_db():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()