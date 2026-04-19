from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.discussion import Discussion
from app.models.user import UserRole
from app.repository.discussion_repo import DiscussionRepository
from app.repository.lesson_repo import LessonRepository
from app.repository.enrollment_repo import EnrollmentRepository
from app.repository.course_repo import CourseRepository


class DiscussionService:

    def __init__(self):
        self.discussion_repo = DiscussionRepository()
        self.lesson_repo = LessonRepository()
        self.enrollment_repo = EnrollmentRepository()
        self.course_repo = CourseRepository()

    async def _check_access(self, db, user, lesson):
        course = await self.course_repo.get_by_id(db, lesson.course_id)

        if user.role == UserRole.ADMIN:
            return

        if user.role == UserRole.INSTRUCTOR and course.owner_id == user.id:
            return

        enrollment = await self.enrollment_repo.get_by_user_course(
            db, user.id, lesson.course_id
        )
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be enrolled to participate in discussions"
            )

    async def create(self, db: AsyncSession, user, lesson_id, message: str, parent_id=None):

        lesson = await self.lesson_repo.get_by_id(db, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        await self._check_access(db, user, lesson)

        if parent_id:
            parent = await self.discussion_repo.get_by_id(db, parent_id)
            if not parent:
                raise HTTPException(status_code=404, detail="Parent comment not found")

            if parent.lesson_id != lesson.id:
                raise HTTPException(status_code=400, detail="Parent comment is not from this lesson")

        discussion = Discussion(
            user_id=user.id,
            lesson_id=lesson_id,
            message=message,
            parent_id=parent_id,
        )

        created = await self.discussion_repo.create(db, discussion)

        return await self.discussion_repo.get_by_id(db, created.id)

    async def get_lesson_discussions(self, db: AsyncSession, user, lesson_id):

        lesson = await self.lesson_repo.get_by_id(db, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        await self._check_access(db, user, lesson)

        return await self.discussion_repo.get_by_lesson(db, lesson_id)

    async def update(self, db: AsyncSession, user, discussion_id, message: str):

        discussion = await self.discussion_repo.get_by_id(db, discussion_id)
        if not discussion:
            raise HTTPException(status_code=404, detail="Comment not found")

        if discussion.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own comments"
            )

        return await self.discussion_repo.update(db, discussion, message)

    async def delete(self, db: AsyncSession, user, discussion_id):

        discussion = await self.discussion_repo.get_by_id(db, discussion_id)
        if not discussion:
            raise HTTPException(status_code=404, detail="Comment not found")

        if discussion.user_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )

        await self.discussion_repo.delete(db, discussion)
        return {"message": "Comment deleted"}