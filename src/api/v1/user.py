from fastapi import APIRouter, Depends

from src.models.user import User
from src.schemas.user import UserIDB
from src.services.auth_deps import get_current_user

router = APIRouter(tags=["auth"])


@router.get("/me", response_model=UserIDB)
async def get_user(user: User = Depends(get_current_user)):
    return user
