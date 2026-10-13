from pydantic_settings import BaseSettings , SettingsConfigDict
from pathlib import Path


# Directly pin the path to the root folder where config.py lives
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"
class Settings(BaseSettings):
    database_name:str
    database_user:str
    database_password:str
    database_host:str
    database_port:str
    secret_key:str
    algorithm:str
    expiration_time:int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
settings = Settings()