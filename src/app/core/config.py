from fastapi import FastAPI
from openai import AsyncClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis


class Config(BaseSettings):
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str

    ACCESS_TOKEN_TTL: int = 16500
    
    model_config = SettingsConfigDict(env_file='.env')

config = Config()
app = FastAPI()
redis_client = Redis()
async_openai_client = AsyncClient(api_key=config.OPENAI_API_KEY,
                                  base_url=config.OPENAI_BASE_URL)
