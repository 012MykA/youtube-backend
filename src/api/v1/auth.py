from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Response

from src.core.config import load_auth_jwt
from src.schemas.token import Token
from src.schemas.user import UserCreate, UserIDB
from src.services.auth import auth_user, create_access_token
from src.services.user_service import UserService, get_user_service

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserIDB)
async def registration(
    user_in: UserCreate, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create(user_in)
    return user


@router.post("/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> Token:
    user = await auth_user(form_data.username, form_data.password, user_service)
    if not user:
        raise HTTPException(401)

    access_token = create_access_token({"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=load_auth_jwt().ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": 200, "message": "Successfully logged out"}
