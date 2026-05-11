"""
An main module for initializing clients
"""

from httpx import AsyncClient
from openai import AsyncOpenAI
from redis.asyncio import Redis

from core.config import config

steos_voice_client = AsyncClient()
async_openai_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY,
                                  base_url=config.OPENAI_BASE_URL)
redis_client = Redis(host=config.REDIS_HOST,
                     port=config.REDIS_PORT,
                     decode_responses=True)