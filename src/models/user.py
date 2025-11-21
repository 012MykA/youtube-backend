from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    username: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
