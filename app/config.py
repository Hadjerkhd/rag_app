from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    PROJECT_NAME: str = "RAG"

    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4.1-nano-2025-04-14"
    OPENAI_API_KEY: SecretStr = SecretStr("willNotWork")

    CHROMA_DB_HOST: str = "chroma"
    CHROMA_DB_PORT: int = 8001
    
    
    PG_DB_HOST: str = "postgres_db"
    PG_DB_PORT: int = 5432
    PG_DB_NAME: str = "researcher_assistantdb"
    PG_DB_USER_NAME: str = "appuser"
    PG_password: str  = "apppassword"
    
    CHUNKS_SIZE: int =1000
    TOP_K_RETRIEVE: int = 5
    
    COLLECTOR_ENDPOINT: str = "http://phoenix:6006/v1/traces"
    OTEL_BSP_SCHEDULE_DELAY_MS: int = 10000
settings = Settings()
