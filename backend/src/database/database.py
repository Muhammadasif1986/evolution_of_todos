from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session, create_engine
from src.config import settings


# Create database engine
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL query logging
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session():
    with Session(engine) as session:
        yield session