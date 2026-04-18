from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment
from app.repository.enrollment_repo import EnrollmentRepository
from app.repository.course_repo import CourseRepository
from app.models.user import UserRole


class EnrollmentService:

    def __init__(
        self,
        enrollment_repo: EnrollmentRepository,
        course_repo: CourseRepository,
    ):
        self.enrollment_repo = enrollment_repo
        self.course_repo = course_repo

    async def enroll(self, db: AsyncSession, user, course_id):

        if user.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can enroll"
            )

        course = await self.course_repo.get_by_id(db, course_id)
        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        existing = await self.enrollment_repo.get_by_user_course(
            db,
            user.id,
            course_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Already enrolled"
            )

        enrollment = Enrollment(
            user_id=user.id,
            course_id=course_id
        )

        return await self.enrollment_repo.create(db, enrollment)

    async def my_courses(self, db: AsyncSession, user):
        return await self.enrollment_repo.get_user_courses(db, user.id)