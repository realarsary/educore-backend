from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from app.schemas.category import CategoryResponse

class CourseBase(BaseModel):
    title: str
    description: str | None = None


class CourseCreate(CourseBase):
    category_id: UUID | None = None


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CourseResponse(CourseBase):
    id: UUID
    owner_id: UUID
    cover_url: str | None = None
    category_id: UUID | None = None
    category: CategoryResponse | None = None

    class Config:
        from_attributes = True