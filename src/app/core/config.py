from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_BASE_URL: str
    OPENAI_API_KEY: str
    DB_URL: str
    
    REDIS_HOST: str
    REDIS_PORT: int

    STEOS_TOKEN: str | None = None


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
