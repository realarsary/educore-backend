from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.user_repo import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def update_me(self, db: AsyncSession, user, data):
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        return await self.user_repo.update(db, user.id, update_data)