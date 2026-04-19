from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.services.discussion_service import DiscussionService
from app.schemas.discussion import DiscussionCreate, DiscussionUpdate, DiscussionResponse

router = APIRouter()

service = DiscussionService()


@router.post("/lessons/{lesson_id}/discussions", response_model=DiscussionResponse)
async def create_discussion(
    lesson_id: UUID,
    data: DiscussionCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.create(db, user, lesson_id, data.message, data.parent_id)


@router.get("/lessons/{lesson_id}/discussions", response_model=List[DiscussionResponse])
async def get_lesson_discussions(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.get_lesson_discussions(db, user, lesson_id)


@router.patch("/discussions/{discussion_id}", response_model=DiscussionResponse)
async def update_discussion(
    discussion_id: UUID,
    data: DiscussionUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.update(db, user, discussion_id, data.message)


@router.delete("/discussions/{discussion_id}")
async def delete_discussion(
    discussion_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await service.delete(db, user, discussion_id)