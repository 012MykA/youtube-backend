from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.user import UserCreate
from src.models.user import User
from src.services.security import get_password_hash
from src.db.session import get_async_session


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session)
