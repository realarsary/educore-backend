from fastapi import HTTPException, status
from app.models.lesson import Lesson
from app.repository.lesson_repo import LessonRepository
from app.repository.course_repo import CourseRepository


class LessonService:

    def __init__(self):
        self.lesson_repo = LessonRepository()
        self.course_repo = CourseRepository()

    async def create_lesson(self, db, data, course_id, user):

        course = await self.course_repo.get_by_id(db, course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if course.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not owner of this course"
            )

        lesson = Lesson(
            title=data.title,
            content=data.content,
            course_id=course_id,
            order=data.order if hasattr(data, "order") else 0
        )

        return await self.lesson_repo.create(db, lesson)

    async def get_course_lessons(self, db, course_id):
        return await self.lesson_repo.get_by_course(db, course_id)