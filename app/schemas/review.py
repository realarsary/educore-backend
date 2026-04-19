from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = None


class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    course_id: UUID
    rating: int
    comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True