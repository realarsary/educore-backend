from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.lesson import Lesson


class LessonRepository:

    async def create(self, db: AsyncSession, lesson: Lesson):
        db.add(lesson)
        await db.commit()
        await db.refresh(lesson)
        return lesson

    async def get_by_course(self, db: AsyncSession, course_id):
        result = await db.execute(
            select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)
        )
        return result.scalars().all()