from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Any


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'PDF Toolbox'
    VERSION: str = '1.0.0'

    # CORS
    BACKEND_CORS_ORIGINS: str = 'http://localhost:5173,http://localhost:3000'

    # File settings
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    MAX_FILES_PER_UPLOAD: int = 20
    ALLOWED_FILE_TYPES: list[str] = ['application/pdf']

    # Storage settings
    STORAGE_DIR: str = 'storage'
    UPLOAD_DIR: str = 'storage/uploads'
    RESULT_DIR: str = 'storage/results'
    FILE_EXPIRE_HOURS: int = 2

    # Processing settings
    MAX_WORKERS: int = 4
    TASK_TIMEOUT: int = 300  # 5 minutes

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',')]

    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
