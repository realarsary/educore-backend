from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUploadResponse
from app.services.lesson_service import LessonService

router = APIRouter()

service = LessonService()


@router.post("/courses/{course_id}/lessons", response_model=LessonUploadResponse)
async def create_lesson(
    course_id: UUID,
    data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    lesson, upload_url = await service.create_lesson(db, data, course_id, user)
    return LessonUploadResponse(lesson=lesson, upload_url=upload_url)


@router.post("/lessons/{lesson_id}/confirm", response_model=LessonResponse)
async def confirm_upload(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await service.confirm_upload(db, lesson_id, user)


@router.get("/courses/{course_id}/lessons", response_model=List[LessonResponse])
async def get_lessons(
    course_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_course_lessons(db, course_id)


@router.get("/lessons/{lesson_id}/video")
async def get_video_url(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_video_url(db, lesson_id)