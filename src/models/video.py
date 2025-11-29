from uuid import uuid4, UUID
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class Video(Base):
    uuid: Mapped[UUID] = mapped_column(unique=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]

    # Statistics
    view_count: Mapped[int] = mapped_column(default=0)
    like_count: Mapped[int] = mapped_column(default=0)
    dislike_count: Mapped[int] = mapped_column(default=0)

    # Dates
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # System
    file_path: Mapped[str] = mapped_column(unique=True)
    file_size: Mapped[int]

    # Relations
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship(back_populates="videos")
