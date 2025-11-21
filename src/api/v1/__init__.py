from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.admin import router as admin_router
from src.api.v1.user import router as user_router

root_router = APIRouter()

root_router.include_router(auth_router)
root_router.include_router(admin_router)
root_router.include_router(user_router)
