from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str