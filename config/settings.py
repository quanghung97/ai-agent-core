from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "AI Agent Core"
    DEBUG: bool = False
    
    # GRPC Config
    GRPC_HOST: str = "localhost"
    GRPC_PORT: int = 50051
    
    # OpenAI Config
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1-mini"
    OPENAI_MODEL_SEARCH: str = "gpt-4o-mini-search-preview"

    # ElevenLabs Config
    ELEVENLABS_API_KEY: str
    
    # Redis Config
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    #ChromaDB Config
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8000
    
    # Agent Config
    MAX_CONCURRENT_USERS: int = 1000
    SESSION_TIMEOUT: int = 3600
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
