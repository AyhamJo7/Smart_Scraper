from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    API_DEBUG: bool = True

    # Scraper Settings
    MAX_CONCURRENT_SCRAPES: int = 5
    REQUEST_TIMEOUT: int = 30
    RETRY_ATTEMPTS: int = 3

    # AI Settings
    OLLAMA_API_URL: str = "http://localhost:11434"
    AI_MODEL: str = "llama2"

    # Database
    DATABASE_URL: str = "sqlite:///./smart_scraper.db"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "scraper.log"

    # Security
    SECRET_KEY: str

    class Config:
        env_file = ".env"

@lru_cache()
def load_config() -> Settings:
    return Settings() 