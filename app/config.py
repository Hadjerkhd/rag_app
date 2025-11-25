from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    PROJECT_NAME: str = "RAG"

    OPENAI_API_BASE: str = "https://lab.iaparc.chapsvision.com/llm-gateway/"
    OPENAI_MODEL: str = "Mistral-Small"
    OPENAI_API_KEY: SecretStr = SecretStr("willNotWork")

    CHROMA_DB_HOST: str = "chroma"
    CHROMA_DB_PORT: int = 8001
    
    
    PG_DB_HOST: str = "postgres_db"
    PG_DB_PORT: int = 5433
    PG_DB_NAME: str = "researcher_assistantdb"
    PG_DB_USER_NAME: str = "appuser"
    PG_password: str  = "apppassword"
    
settings = Settings()
