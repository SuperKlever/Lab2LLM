from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    model: str = Field(default="gpt-4o-mini")

    BASE_URL: str = Field(default=os.getenv("BASE_URL"))
    API_KEY: str = Field(default=os.getenv("API_KEY"))
    MODEL_NAME: str = Field(default="qwen3-32b")
    MAX_RETRIES: int = Field(default=1)
    BASE_TEMPERATURE: float = Field(default=0.7)
    MAX_TEMPERATURE: float = Field(default=1)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Settings = Settings()
