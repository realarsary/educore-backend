from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.repository.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin

router = APIRouter()

user_repo = UserRepository()
auth_service = AuthService(user_repo)


@router.post("/register")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.register(db, user_data.email, user_data.username, user_data.password, user_data.role)


@router.post("/login")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.login(db, user_data.email, user_data.password)