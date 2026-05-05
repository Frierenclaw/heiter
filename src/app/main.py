from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api.v1.endpoints import base_api_router
from core.config import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    TORTOISE_ORM
)

app.include_router(base_api_router)


