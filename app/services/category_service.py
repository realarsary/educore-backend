from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repository.category_repo import CategoryRepository


class CategoryService:

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create(self, db: AsyncSession, name: str, description: str):
        existing = await self.repo.get_by_name(db, name)
        if existing:
            raise HTTPException(status_code=400, detail="Category already exists")

        category = Category(name=name, description=description)
        return await self.repo.create(db, category)

    async def get_all(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def update(self, db: AsyncSession, category_id, data: dict):
        category = await self.repo.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return await self.repo.update(db, category_id, data)