from fastapi import HTTPException, status

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

from app.repository.user_repo import UserRepository
from app.models.user import User


class AuthService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo


    async def register(self, db, email: str, username: str, password: str, role: str):

        existing = await self.user_repo.get_by_email(db, email)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

        user = User(
            email=email,
            username=username,
            hashed_password=hash_password(password),
            role=role
        )

        return await self.user_repo.create(db, user)


    async def login(self, db, email: str, password: str):

        user = await self.user_repo.get_by_email(db, email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }