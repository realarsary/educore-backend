import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, UniqueConstraint, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    course = relationship("Course")

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_user_course_review"),
    )