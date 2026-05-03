from fastapi import FastAPI
from api.v1.endpoints import base_api_router

async def lifespan(_) -> iter:
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(base_api_router)


