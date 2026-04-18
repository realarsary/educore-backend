from sqlalchemy import select, func, cast, text

from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.progress import LessonProgress
from app.models.lesson import Lesson, LessonStatus


class ProgressRepository:

    async def get_by_user_lesson(self, db: AsyncSession, user_id, lesson_id):
        result = await db.execute(
            select(LessonProgress).where(
                LessonProgress.user_id == user_id,
                LessonProgress.lesson_id == lesson_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, progress: LessonProgress):
        db.add(progress)
        await db.commit()
        await db.refresh(progress)
        return progress

    async def delete(self, db: AsyncSession, progress: LessonProgress):
        await db.delete(progress)
        await db.commit()

    async def get_total_count(self, db: AsyncSession, course_id):
        result = await db.execute(
            select(func.count(Lesson.id)).where(
                Lesson.course_id == course_id,
                Lesson.status == text("'PUBLISHED'"),
            )
        )
        return result.scalar()

    async def get_completed_count(self, db: AsyncSession, user_id, course_id):
        result = await db.execute(
            select(func.count(LessonProgress.id))
            .join(Lesson, Lesson.id == LessonProgress.lesson_id)
            .where(
                LessonProgress.user_id == user_id,
                Lesson.course_id == course_id,
                Lesson.status == text("'PUBLISHED'"),
            )
        )
        return result.scalar()