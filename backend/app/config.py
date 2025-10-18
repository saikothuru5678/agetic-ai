from typing import Optional
from pydantic_settings import BaseSettings

from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Agentic AI Parent–University Engagement Platform"
    database_url: str = "sqlite:///app_data/feedback.db"
    openai_api_key: Optional[str] = None  # if None, app will use heuristic fallback
    load_sample_on_boot: bool = True

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()