from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.course import Course


class CourseRepository:

    async def create(self, db: AsyncSession, course: Course):
        db.add(course)
        await db.commit()
        await db.refresh(course)
        return course

    async def get_by_id(self, db: AsyncSession, course_id):
        result = await db.execute(
            select(Course).where(Course.id == course_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Course))
        return result.scalars().all()

    async def get_by_owner(self, db: AsyncSession, owner_id):
        result = await db.execute(
            select(Course).where(Course.owner_id == owner_id)
        )
        return result.scalars().all()

    async def update(self, db: AsyncSession, course_id: int, data: dict):
        query = (
            update(Course)
            .where(Course.id == course_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await db.commit()
        return await self.get_by_id(db, course_id)

    async def delete(self, db: AsyncSession, course_id: int):
        query = delete(Course).where(Course.id == course_id)
        await db.execute(query)
        await db.commit()
        return True