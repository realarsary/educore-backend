from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import update as sa_update

from app.models.category import Category


class CategoryRepository:

    async def create(self, db: AsyncSession, category: Category):
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    async def get_all(self, db: AsyncSession):
        result = await db.execute(
            select(Category).where(Category.is_active == True)
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, category_id):
        result = await db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, db: AsyncSession, name: str):
        result = await db.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, category_id, data: dict):
        await db.execute(
            sa_update(Category)
            .where(Category.id == category_id)
            .values(**data)
        )
        await db.commit()
        return await self.get_by_id(db, category_id)