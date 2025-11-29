from uuid import UUID, uuid4

from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.video import Video
from src.db.session import get_async_session
from src.schemas.video import VideoCreate

VIDEOS_DB_PATH = "E:/videos-db"


class VideoService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_video(self, uuid: UUID) -> Video | None:
        stmt = select(Video).where(Video.uuid == uuid)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_video(self, video_in: VideoCreate, video_file: UploadFile, user_id: int) -> Video:
        # Video
        video_uuid = uuid4()
        file_path = f"{VIDEOS_DB_PATH}/{video_uuid}-{video_file.filename}"
        file_content = await video_file.read()

        with open(file_path, "wb") as f:
            f.write(file_content)

        video = Video(
            uuid=video_uuid,
            title=video_in.title,
            description=video_in.description,
            file_size=video_file.size,
            file_path=file_path,
            user_id=user_id
        )

        self.session.add(video)
        await self.session.commit()
        await self.session.refresh(video)
        return video


def get_video_service(session: AsyncSession = Depends(get_async_session)) -> VideoService:
    return VideoService(session)
