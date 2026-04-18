from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.repository.course_repo import CourseRepository
from app.repository.enrollment_repo import EnrollmentRepository
from app.models.user import UserRole


class CourseService:

    def __init__(self, course_repo: CourseRepository, enrollment_repo: EnrollmentRepository):
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo

    async def create_course(self, db: AsyncSession, user, title: str, description: str):

        if user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors or admins can create courses"
            )

        course = Course(
            title=title,
            description=description,
            owner_id=user.id,
        )

        return await self.course_repo.create(db, course)

    async def get_course(self, db: AsyncSession, course_id):
        course = await self.course_repo.get_by_id(db, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        return course

    async def get_courses(self, db: AsyncSession):
        return await self.course_repo.get_all(db)
    

    async def update_course(self, db: AsyncSession, user, course_id: int, update_data: dict):
        course = await self.get_course(db, course_id)

        if course.owner_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to update this course"
            )

        return await self.course_repo.update(db, course_id, update_data)

    async def delete_course(self, db: AsyncSession, user, course_id: int):
        course = await self.get_course(db, course_id)

        if course.owner_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to delete this course"
            )

        return await self.course_repo.delete(db, course_id)


    async def get_my_courses(self, db: AsyncSession, user):
        return await self.course_repo.get_by_owner(db, user.id)


    async def get_course_students(self, db: AsyncSession, user, course_id):

        course = await self.course_repo.get_by_id(db, course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if course.owner_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Not allowed"
            )

        enrollments = await self.enrollment_repo.get_course_students(db, course_id)

        return [e.user for e in enrollments]
    
    async def search_courses(self, db: AsyncSession, search: str = None, category_id = None):
        return await self.course_repo.search(db, search, category_id)