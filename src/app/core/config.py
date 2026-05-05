from fastapi import FastAPI
from openai import AsyncClient
from pydantic_settings import BaseSettings
from redis.asyncio import Redis


class Config(BaseSettings):
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str
    DB_URL: str
    
    REDIS_HOST: str
    REDIS_PORT: int

    ACCESS_TOKEN_TTL: int = 16500
    
config = Config()

TORTOISE_ORM = {
    'connections': {
        'default': config.DB_URL
    },
    'minsize': 8,
    'maxsize': 30,
    
    'apps': {
        'models': {
            'models': [
                'models.user'
            ],
            'migrations': 'models.migrations',
            'default_connection': 'default'
        }
    }
}

app = FastAPI()
redis_client = Redis(host=config.REDIS_HOST,
                     port=config.REDIS_PORT,
                     decode_responses=True)
async_openai_client = AsyncClient(api_key=config.OPENAI_API_KEY,
                                  base_url=config.OPENAI_BASE_URL)
