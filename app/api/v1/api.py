from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import course

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(course.router, prefix="/courses", tags=["courses"])