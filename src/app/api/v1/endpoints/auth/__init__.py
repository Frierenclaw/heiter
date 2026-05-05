from fastapi import APIRouter

from api.v1.endpoints.auth import login, register

base_auth_router = APIRouter(prefix='/auth')

base_auth_router.include_router(router=login.router,
                                tags=['Login'])
base_auth_router.include_router(router=register.router,
                                tags=['Register'])