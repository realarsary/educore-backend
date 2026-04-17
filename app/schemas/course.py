from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    title: str
    description: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CourseResponse(CourseBase):
    id: UUID
    owner_id: UUID

    class Config:
        from_attributes = True