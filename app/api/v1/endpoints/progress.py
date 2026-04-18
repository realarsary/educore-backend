from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.services.progress_service import ProgressService
from app.schemas.progress import LessonProgressResponse, CourseProgressResponse

router = APIRouter()

service = ProgressService()


@router.post("/lessons/{lesson_id}/complete", response_model=LessonProgressResponse)
async def complete_lesson(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.complete_lesson(db, user, lesson_id)


@router.delete("/lessons/{lesson_id}/complete")
async def uncomplete_lesson(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.uncomplete_lesson(db, user, lesson_id)


@router.get("/courses/{course_id}/progress", response_model=CourseProgressResponse)
async def get_course_progress(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.get_course_progress(db, user, course_id)