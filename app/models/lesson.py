import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)

    order = Column(Integer, default=0)

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", backref="lessons")