from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.core.config import load_auth_jwt
from src.services.user_service import UserService, get_user_service
from src.services.security import verify_password
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


async def auth_user(email: str, password: str, user_service: UserService) -> User | None:
    user = await user_service.get_by_email(email)

    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=load_auth_jwt().ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=load_auth_jwt().private_key_path.read_text(),
        algorithm=load_auth_jwt().ALGORITHM
    )
    return encoded_jwt
