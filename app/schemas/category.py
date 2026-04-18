from pydantic import BaseModel
from uuid import UUID


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    is_active: bool

    class Config:
        from_attributes = True