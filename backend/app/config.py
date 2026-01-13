"""
Configuration settings using environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "AI Call Summarizer"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/call_assistant"

    # JWT Authentication
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # Object Storage (S3-compatible)
    storage_endpoint: str = ""
    storage_access_key: str = ""
    storage_secret_key: str = ""
    storage_bucket: str = "call-recordings"

    # AI Services
    openai_api_key: str = ""
    whisper_model: str = "whisper-1"

    # Redis (for background tasks)
    redis_url: str = "redis://localhost:6379/0"

    # VoIP/SIP
    sip_server: str = ""
    sip_username: str = ""
    sip_password: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
