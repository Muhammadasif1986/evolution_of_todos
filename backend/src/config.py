from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://todo_user:todo_password@localhost:5432/todo_db"

    # Auth
    secret_key: str = "your-super-secret-key-change-in-production"
    better_auth_secret: str = ""  # From environment variable
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
