from fastapi import FastAPI
from api.v1.endpoints import base_api_router

from tortoise import Tortoise

async def lifespan(_) -> iter:
    await Tortoise.init()

    yield

    await Tortoise.close_connections()
    
app = FastAPI(lifespan=lifespan)
app.include_router(base_api_router)


