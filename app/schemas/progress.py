from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class LessonProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    lesson_id: UUID
    completed_at: datetime

    class Config:
        from_attributes = True


class CourseProgressResponse(BaseModel):
    course_id: UUID
    total_lessons: int
    completed_lessons: int
    percentage: float