from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.models.user import UserRole
from app.repository.review_repo import ReviewRepository
from app.repository.enrollment_repo import EnrollmentRepository


class ReviewService:

    def __init__(self):
        self.review_repo = ReviewRepository()
        self.enrollment_repo = EnrollmentRepository()

    async def create_review(self, db: AsyncSession, user, course_id, rating: int, comment: str):

        if user.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can leave reviews"
            )

        enrollment = await self.enrollment_repo.get_by_user_course(db, user.id, course_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be enrolled to leave a review"
            )

        existing = await self.review_repo.get_by_user_course(db, user.id, course_id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="You have already reviewed this course"
            )

        review = Review(
            user_id=user.id,
            course_id=course_id,
            rating=rating,
            comment=comment,
        )

        return await self.review_repo.create(db, review)

    async def get_course_reviews(self, db: AsyncSession, course_id):
        return await self.review_repo.get_by_course(db, course_id)

    async def get_course_rating(self, db: AsyncSession, course_id):
        avg_rating, total = await self.review_repo.get_course_rating(db, course_id)
        return {
            "course_id": course_id,
            "average_rating": avg_rating,
            "total_reviews": total,
        }

    async def update_review(self, db: AsyncSession, user, review_id, data: dict):
        review = await self.review_repo.get_by_id(db, review_id)

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        if review.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )

        return await self.review_repo.update(db, review_id, data)

    async def delete_review(self, db: AsyncSession, user, review_id):
        review = await self.review_repo.get_by_id(db, review_id)

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        if review.user_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )

        await self.review_repo.delete(db, review)
        return {"message": "Review deleted"}