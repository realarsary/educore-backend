from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.review import Review


class ReviewRepository:

    async def create(self, db: AsyncSession, review: Review):
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    async def get_by_id(self, db: AsyncSession, review_id):
        result = await db.execute(
            select(Review).where(Review.id == review_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_course(self, db: AsyncSession, user_id, course_id):
        result = await db.execute(
            select(Review).where(
                Review.user_id == user_id,
                Review.course_id == course_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_course(self, db: AsyncSession, course_id):
        result = await db.execute(
            select(Review)
            .options(selectinload(Review.user))
            .where(Review.course_id == course_id)
            .order_by(Review.created_at.desc())
        )
        return result.scalars().all()

    async def get_course_rating(self, db: AsyncSession, course_id):
        result = await db.execute(
            select(func.avg(Review.rating), func.count(Review.id))
            .where(Review.course_id == course_id)
        )
        avg_rating, total = result.one()
        return round(float(avg_rating), 2) if avg_rating else 0.0, total

    async def update(self, db: AsyncSession, review_id, data: dict):
        review = await self.get_by_id(db, review_id)
        for key, value in data.items():
            setattr(review, key, value)
        await db.commit()
        await db.refresh(review)
        return review

    async def delete(self, db: AsyncSession, review: Review):
        await db.delete(review)
        await db.commit()