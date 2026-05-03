from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    pass

config = Config()
app = FastAPI()
