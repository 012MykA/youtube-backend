from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VideoCreate(BaseModel):
    title: str
    description: str


class VideoIDB(BaseModel):
    uuid: UUID
    title: str
    description: str

    # Statistics
    view_count: int
    like_count: int
    dislike_count: int

    # Dates
    created_at: datetime
    updated_at: datetime

    # System
    file_path: str
    file_size: int

    # Relations
    user_id: int

    model_config = ConfigDict(from_attributes=True)
