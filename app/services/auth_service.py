from fastapi import HTTPException, status
from app.core.redis_helpers import delete_refresh
from app.core.security import get_user_id_from_token

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
)

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

from app.core.redis_helpers import get_stored_refresh, save_refresh
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
        
        await save_refresh(user.id, refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


    async def refresh_tokens(self, db, refresh_token: str):

        payload = decode_refresh_token(refresh_token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")

        stored_token = await get_stored_refresh(user_id)

        if stored_token != refresh_token:
            raise HTTPException(status_code=401, detail="Token revoked")

        user = await self.user_repo.get_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_access = create_access_token({"sub": user_id})
        new_refresh = create_refresh_token({"sub": user_id})

        await save_refresh(user_id, new_refresh)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }
    async def logout(self, refresh_token: str):

        payload = decode_refresh_token(refresh_token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")

        await delete_refresh(user_id)

        return {"message": "Logged out successfully"}