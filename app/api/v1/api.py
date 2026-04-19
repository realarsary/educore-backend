from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import course
from app.api.v1.endpoints import enrollment
from app.api.v1.endpoints import lesson
from app.api.v1.endpoints import user
from app.api.v1.endpoints import category
from app.api.v1.endpoints import progress
from app.api.v1.endpoints import review
from app.api.v1.endpoints import discussion


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(course.router, prefix="/courses", tags=["courses"])
api_router.include_router(enrollment.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(lesson.router, prefix="", tags=["lessons"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(review.router, prefix="", tags=["reviews"])
api_router.include_router(discussion.router, prefix="", tags=["discussions"])