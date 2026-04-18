from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.progress import LessonProgress
from app.models.lesson import LessonStatus
from app.models.user import UserRole
from app.repository.progress_repo import ProgressRepository
from app.repository.lesson_repo import LessonRepository
from app.repository.enrollment_repo import EnrollmentRepository
from app.schemas.progress import CourseProgressResponse


class ProgressService:

    def __init__(self):
        self.progress_repo = ProgressRepository()
        self.lesson_repo = LessonRepository()
        self.enrollment_repo = EnrollmentRepository()

    async def complete_lesson(self, db: AsyncSession, user, lesson_id):

        if user.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can track progress"
            )

        lesson = await self.lesson_repo.get_by_id(db, lesson_id)

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        if lesson.status != LessonStatus.PUBLISHED:
            raise HTTPException(status_code=400, detail="Lesson is not published yet")

        enrollment = await self.enrollment_repo.get_by_user_course(
            db, user.id, lesson.course_id
        )

        if not enrollment:
            raise HTTPException(
                status_code=403,
                detail="You are not enrolled in this course"
            )

        existing = await self.progress_repo.get_by_user_lesson(db, user.id, lesson_id)

        if existing:
            raise HTTPException(status_code=400, detail="Lesson already completed")

        progress = LessonProgress(user_id=user.id, lesson_id=lesson_id)
        return await self.progress_repo.create(db, progress)

    async def uncomplete_lesson(self, db: AsyncSession, user, lesson_id):

        if user.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can track progress"
            )

        progress = await self.progress_repo.get_by_user_lesson(db, user.id, lesson_id)

        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")

        await self.progress_repo.delete(db, progress)
        return {"message": "Lesson marked as incomplete"}

    async def get_course_progress(self, db: AsyncSession, user, course_id):

        enrollment = await self.enrollment_repo.get_by_user_course(
            db, user.id, course_id
        )

        if not enrollment:
            raise HTTPException(
                status_code=403,
                detail="You are not enrolled in this course"
            )

        total = await self.progress_repo.get_total_count(db, course_id)
        completed = await self.progress_repo.get_completed_count(db, user.id, course_id)

        percentage = round((completed / total * 100), 2) if total > 0 else 0.0

        return CourseProgressResponse(
            course_id=course_id,
            total_lessons=total,
            completed_lessons=completed,
            percentage=percentage,
        )