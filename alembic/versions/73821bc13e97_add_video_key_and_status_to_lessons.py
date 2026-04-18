"""add video_key and status to lessons

Revision ID: 73821bc13e97
Revises: 266b355ca08b
Create Date: 2026-04-18 15:43:04.515948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73821bc13e97'
down_revision: Union[str, Sequence[str], None] = '266b355ca08b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. добавить video_key
    op.add_column(
        "lessons",
        sa.Column("video_key", sa.String(), nullable=True)
    )

    # 2. сначала добавляем как STRING (без enum)
    op.add_column(
        "lessons",
        sa.Column("status", sa.String(), nullable=True)
    )

    # 3. заполняем старые строки
    op.execute("""
        UPDATE lessons
        SET status = 'DRAFT'
        WHERE status IS NULL
    """)

    # 4. делаем NOT NULL
    op.alter_column("lessons", "status", nullable=False)

    # 5. ограничиваем значения (PRO way вместо ENUM)
    op.create_check_constraint(
        "ck_lessons_status",
        "lessons",
        "status IN ('DRAFT', 'PUBLISHED')"
    )


def downgrade():
    op.drop_constraint("ck_lessons_status", "lessons", type_="check")
    op.drop_column("lessons", "status")
    op.drop_column("lessons", "video_key")


