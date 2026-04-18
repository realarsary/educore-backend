import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Lesson, LessonStatus
from app.repository.lesson_repo import LessonRepository
from app.repository.course_repo import CourseRepository
from app.services.file_service import FileService
from app.core.minio import minio_client
from app.schemas.lesson import LessonCreate


class LessonService:

    def __init__(self):
        self.lesson_repo = LessonRepository()
        self.course_repo = CourseRepository()
        self.file_service = FileService(minio_client)

    async def create_lesson(self, db: AsyncSession, data: LessonCreate, course_id, user):

        course = await self.course_repo.get_by_id(db, course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if course.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not owner of this course"
            )

        video_key = f"lessons/{course_id}/{uuid.uuid4()}.mp4"

        lesson = Lesson(
            title=data.title,
            content=data.content,
            course_id=course_id,
            order=data.order,
            video_key=video_key,
            status=LessonStatus.DRAFT,
        )

        lesson = await self.lesson_repo.create(db, lesson)

        upload_url = await self.file_service.get_upload_url(video_key)

        return lesson, upload_url

    async def confirm_upload(self, db: AsyncSession, lesson_id, user):

        lesson = await self.lesson_repo.get_by_id(db, lesson_id)

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        course = await self.course_repo.get_by_id(db, lesson.course_id)

        if course.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        exists = await self.file_service.file_exists(lesson.video_key)

        if not exists:
            raise HTTPException(
                status_code=400,
                detail="Video not uploaded yet"
            )

        return await self.lesson_repo.update_status(db, lesson_id, LessonStatus.PUBLISHED)

    async def get_course_lessons(self, db: AsyncSession, course_id):
        return await self.lesson_repo.get_by_course(db, course_id)

    async def get_video_url(self, db: AsyncSession, lesson_id):

        lesson = await self.lesson_repo.get_by_id(db, lesson_id)

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        if lesson.status != LessonStatus.PUBLISHED:
            raise HTTPException(status_code=400, detail="Video not ready")

        url = await self.file_service.get_download_url(lesson.video_key)

        return {"url": url}