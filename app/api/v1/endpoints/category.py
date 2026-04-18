from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.core.permissions import require_role
from app.models.user import UserRole
from app.repository.category_repo import CategoryRepository
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter()

repo = CategoryRepository()
service = CategoryService(repo)


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await service.get_all(db)


@router.post("/", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN)),
):
    return await service.create(db, data.name, data.description)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN)),
):
    return await service.update(db, category_id, data.model_dump(exclude_unset=True))


@router.delete("/{category_id}", response_model=CategoryResponse)
async def deactivate_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN)),
):
    return await service.update(db, category_id, {"is_active": False})