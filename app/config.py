from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    PROJECT_NAME: str = "RAG"

    OPENAI_API_BASE: str = "https://lab.iaparc.chapsvision.com/llm-gateway/"
    OPENAI_MODEL: str = "Mistral-Small"
    OPENAI_API_KEY: SecretStr = SecretStr("willNotWork")

    DB_HOST: str = "chroma"
    DB_PORT: int = 8001
    
settings = Settings()
