from typing import Optional
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    APP_DATABASE_URL:str
    ALEMBIC_DATABASE_URL:str

    class Config:
        env_file = "project_sync_backend/.env"
        extra = "allow"

settings=Settings()