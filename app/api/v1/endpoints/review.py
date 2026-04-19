from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.services.review_service import ReviewService
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter()

service = ReviewService()


@router.post("/courses/{course_id}/reviews", response_model=ReviewResponse)
async def create_review(
    course_id: UUID,
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.create_review(db, user, course_id, data.rating, data.comment)


@router.get("/courses/{course_id}/reviews", response_model=List[ReviewResponse])
async def get_course_reviews(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_course_reviews(db, course_id)


@router.get("/courses/{course_id}/rating")
async def get_course_rating(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_course_rating(db, course_id)


@router.patch("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: UUID,
    data: ReviewUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.update_review(db, user, review_id, data.model_dump(exclude_unset=True))


@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.delete_review(db, user, review_id)