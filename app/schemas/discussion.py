from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class DiscussionCreate(BaseModel):
    message: str
    parent_id: UUID | None = None


class DiscussionUpdate(BaseModel):
    message: str


class DiscussionResponse(BaseModel):
    id: UUID
    user_id: UUID
    lesson_id: UUID
    parent_id: UUID | None
    message: str
    created_at: datetime
    replies: List["DiscussionResponse"] = []

    class Config:
        from_attributes = True


DiscussionResponse.model_rebuild()