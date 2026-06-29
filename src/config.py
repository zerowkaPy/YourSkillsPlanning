import logging
import sys

from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def setup_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=r"D:\Code\YourSkillsPlanning\.env",
        env_file_encoding="utf-8"
    )
    pg_dsn: PostgresDsn = Field(validation_alias="POSTGRES_DSN")
    gemini_api_key: str = Field(validation_alias="Gemini_Api_Key")
    jwt_secret_key: str = Field(validation_alias="JWT_SECRET_KEY")
    my_api_key: str = Field(validation_alias="MY_API_KEY")
    
settings = Settings() # type: ignore