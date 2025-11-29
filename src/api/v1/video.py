from uuid import UUID
import re

from fastapi import (
    APIRouter, Request, HTTPException, Depends,
    UploadFile, File
)
from fastapi.responses import StreamingResponse

from src.services.auth_deps import get_current_user
from src.services.video_service import get_video_service, VideoService
from src.services.file_service import get_file_iterator
from src.schemas.video import VideoCreate, VideoIDB
from src.models.user import User

router = APIRouter(tags=["Video"])


@router.post("/upload-video", response_model=VideoIDB)
async def upload_video(
        video_in: VideoCreate = Depends(), video_file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        video_service: VideoService = Depends(get_video_service),
):
    if not video_file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Invalid video type")

    video = await video_service.create_video(video_in, video_file, user.id)
    return video


@router.get("/watch")
async def watch(v: UUID, request: Request, video_service: VideoService = Depends(get_video_service)):
    video = await video_service.get_video(v)

    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    range_header = request.headers.get("Range")
    if range_header:
        # Video parts
        match_header = re.search(r"bytes=(\d+)-(\d*)", range_header)

        if not match_header:
            raise HTTPException(status_code=400, detail="Invalid Range header")

        start_str, end_str = match_header.groups()
        start = int(start_str) if start_str else 0

        if end_str:
            end = int(end_str)
        else:
            end = video.file_size - 1

        if start >= video.file_size or end >= video.file_size or start > end:
            return StreamingResponse(
                content=[],
                status_code=416,
                headers={"Content-Range": f"bytes {start}-{end}/{video.file_size}"}
            )

        content_length = end - start + 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{video.file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": "video/mp4",
        }

        video_iterator = get_file_iterator(video.file_path, start, end)
        return StreamingResponse(
            content=video_iterator,
            status_code=206,
            headers=headers
        )

    else:
        # Full video
        headers = {
            "Content-Length": str(video.file_size),
            "Content-Type": "video/mp4",
            "Accept-Ranges": "bytes",
        }

        media_iterator = get_file_iterator(video.file_path, 0, video.file_size)

        return StreamingResponse(
            content=media_iterator,
            status_code=200,
            headers=headers,
        )
