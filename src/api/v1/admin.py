from fastapi import APIRouter, Depends

from src.services.user_service import UserService, get_user_service
from src.schemas.user import (
    UserCreate,
    UserIDB,
)

router = APIRouter(tags=["Admin"])


@router.post("/users", response_model=UserIDB)
async def create_user(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create(user_in)


@router.get("/users", response_model=list[UserIDB])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()
