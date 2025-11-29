import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, Request

from src.core.config import load_auth_jwt

from src.models.user import User
from src.services.user_service import UserService, get_user_service


async def get_current_user(
    request: Request, user_service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    if token.startswith("Bearer "):
        token = token[7:]

    try:
        payload = jwt.decode(
            token,
            load_auth_jwt().public_key_path.read_text(),
            algorithms=[load_auth_jwt().ALGORITHM],
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = await user_service.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user
