from pydantic import BaseModel
from uuid import UUID


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

    class Config:
        from_attributes = True