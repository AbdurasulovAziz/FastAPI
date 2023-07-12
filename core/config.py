
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = AppSettings()
