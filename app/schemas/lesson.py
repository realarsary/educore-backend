from pydantic import BaseModel
from uuid import UUID
from enum import Enum


class LessonStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class LessonCreate(BaseModel):
    title: str
    content: str | None = None
    order: int = 0


class LessonResponse(BaseModel):
    id: UUID
    title: str
    content: str | None
    order: int
    course_id: UUID
    video_key: str | None
    status: LessonStatus

    class Config:
        from_attributes = True


class LessonUploadResponse(BaseModel):
    lesson: LessonResponse
    upload_url: str