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

    # AI Provider
    gemini_api_key: Optional[str] = None  # From environment variable
    openrouter_api_key: Optional[str] = None  # From environment variable

    # Additional AI settings
    base_url: Optional[str] = None  # From environment variable
    model: Optional[str] = None  # From environment variable (using MODEL)
    base_url_: Optional[str] = None  # From environment variable (using BASE_URL)
    model_: Optional[str] = None  # From environment variable (using MODEL_)

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Additional settings that might be in the environment
    environment: Optional[str] = "development"
    debug: Optional[bool] = True

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow additional fields not explicitly defined


settings = Settings()
