from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import AsyncClient

class Config(BaseSettings):
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file='.env')

config = Config()
app = FastAPI()

async_openai_client = AsyncClient(api_key=config.OPENAI_API_KEY,
                                  base_url=config.OPENAI_BASE_URL)
