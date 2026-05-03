from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file='.env')

config = Config()
app = FastAPI()
