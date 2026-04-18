from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from app.models.enrollment import Enrollment


class EnrollmentRepository:

    async def create(self, db: AsyncSession, enrollment: Enrollment):
        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)
        return enrollment

    async def get_by_user_course(self, db: AsyncSession, user_id, course_id):
        result = await db.execute(
            select(Enrollment).where(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id
            )
        )
        return result.scalar_one_or_none()

    async def get_user_courses(self, db: AsyncSession, user_id):
        result = await db.execute(
            select(Enrollment)
            .options(selectinload(Enrollment.course)) 
            .where(Enrollment.user_id == user_id)
        )
        return result.scalars().all()
   

    async def get_course_students(self, db: AsyncSession, course_id):
        result = await db.execute(
            select(Enrollment)
            .options(selectinload(Enrollment.user))  # 🔥 важно
            .where(Enrollment.course_id == course_id)
        )
        return result.scalars().all()