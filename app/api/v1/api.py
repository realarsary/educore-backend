from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import course
from app.api.v1.endpoints import enrollment
from app.api.v1.endpoints import lesson

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(course.router, prefix="/courses", tags=["courses"])
api_router.include_router(enrollment.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(lesson.router, prefix="", tags=["lessons"])