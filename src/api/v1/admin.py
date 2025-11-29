import os
import glob

from fastapi import APIRouter, Depends

from src.services.user_service import UserService, get_user_service
from src.schemas.user import (
    UserCreate,
    UserIDB,
)

# TODO: remove
from src.db.session import drop_db

router = APIRouter(tags=["Admin"])


@router.post("/users", response_model=UserIDB)
async def create_user(
    user_in: UserCreate, user_service: UserService = Depends(get_user_service)
):
    return await user_service.create(user_in)


@router.get("/users", response_model=list[UserIDB])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()


# TODO: remove
@router.post("/reset-db")
async def reset_db():
    await drop_db()

    files = glob.glob("E:/videos-db/*")
    for f in files:
        os.remove(f)

    return {"message": "Database reset"}
