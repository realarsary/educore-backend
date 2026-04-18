from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.lesson import LessonCreate
from app.services.lesson_service import LessonService

router = APIRouter()

service = LessonService()


@router.post("/courses/{course_id}/lessons")
async def create_lesson(
    course_id,
    data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service.create_lesson(db, data, course_id, user)


@router.get("/courses/{course_id}/lessons")
async def get_lessons(
    course_id,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_course_lessons(db, course_id)