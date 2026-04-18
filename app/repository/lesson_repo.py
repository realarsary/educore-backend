from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

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
    
    async def get_by_id(self, db: AsyncSession, lesson_id):
        result = await db.execute(
            select(Lesson).where(Lesson.id == lesson_id)
        )
        return result.scalar_one_or_none()

    async def update_status(self, db: AsyncSession, lesson_id, status):
        await db.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(status=status)
        )
        await db.commit()
        return await self.get_by_id(db, lesson_id)