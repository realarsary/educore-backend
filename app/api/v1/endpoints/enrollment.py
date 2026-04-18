from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.services.enrollment_service import EnrollmentService
from app.repository.enrollment_repo import EnrollmentRepository
from app.repository.course_repo import CourseRepository
from app.schemas.course import CourseResponse


router = APIRouter()

enrollment_repo = EnrollmentRepository()
course_repo = CourseRepository()
enrollment_service = EnrollmentService(enrollment_repo, course_repo)


@router.post("/{course_id}")
async def enroll(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await enrollment_service.enroll(db, user, course_id)


@router.get("/me", response_model=List[CourseResponse])
async def my_courses(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    enrollments = await enrollment_service.my_courses(db, user)

    return [e.course for e in enrollments]