from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.discussion import Discussion


class DiscussionRepository:

    async def create(self, db: AsyncSession, discussion: Discussion):
        db.add(discussion)
        await db.commit()
        await db.refresh(discussion)
        return discussion

    async def get_by_id(self, db: AsyncSession, discussion_id):
        result = await db.execute(
            select(Discussion)
            .options(
                selectinload(Discussion.replies)
                    .selectinload(Discussion.replies),

                selectinload(Discussion.replies)
                    .selectinload(Discussion.user),

                selectinload(Discussion.user),
            )
            .where(Discussion.id == discussion_id)
        )
        return result.scalar_one_or_none()

    async def get_by_lesson(self, db: AsyncSession, lesson_id):
        result = await db.execute(
            select(Discussion)
            .options(
                selectinload(Discussion.replies)
                    .selectinload(Discussion.replies),  # 2 уровень

                selectinload(Discussion.replies)
                    .selectinload(Discussion.user),

                selectinload(Discussion.user),
            )
            .where(
                Discussion.lesson_id == lesson_id,
                Discussion.parent_id == None,
            )
            .order_by(Discussion.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, db: AsyncSession, discussion: Discussion, message: str):
        discussion.message = message
        await db.commit()
        await db.refresh(discussion)
        return discussion

    async def delete(self, db: AsyncSession, discussion: Discussion):
        await db.delete(discussion)
        await db.commit()