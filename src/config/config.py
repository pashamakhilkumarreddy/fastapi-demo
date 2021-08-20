import config
from pydantic import BaseSettings


class Config(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 5000
    LOG_LEVEL: str = 'info'
    API_URL: str = 'https://jsonplaceholder.typicode.com'

    class Config:
        env_file = 'fastapi-demo/.env'


config = Config()
