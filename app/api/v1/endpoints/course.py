from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from app.api.deps import get_db, get_current_user
from app.services.course_service import CourseService
from app.repository.course_repo import CourseRepository
from app.repository.enrollment_repo import EnrollmentRepository
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.schemas.user import UserResponse
router = APIRouter()

course_repo = CourseRepository()
enrollment_repo = EnrollmentRepository()
course_service = CourseService(course_repo, enrollment_repo)


@router.post("/", response_model=CourseResponse)
async def create_course(
    data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await course_service.create_course(
        db,
        user,
        data.title,
        data.description
    )


@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    db: AsyncSession = Depends(get_db),
):
    return await course_service.get_courses(db)


@router.get("/me", response_model=List[CourseResponse])
async def my_courses(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await course_service.get_my_courses(db, user)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id,
    db: AsyncSession = Depends(get_db),
):
    return await course_service.get_course(db, course_id)


@router.patch("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: UUID,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await course_service.update_course(
        db, 
        user, 
        course_id, 
        data.model_dump(exclude_unset=True)
    )


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    await course_service.delete_course(db, user, course_id)
    return {"detail": "Course deleted"}


@router.get("/{course_id}/students", response_model=List[UserResponse])
async def course_students(
    course_id,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await course_service.get_course_students(db, user, course_id)