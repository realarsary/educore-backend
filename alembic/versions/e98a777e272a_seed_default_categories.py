"""seed default categories

Revision ID: e98a777e272a
Revises: 53625e49a6e5
Create Date: 2026-04-18 21:30:12.784658
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid

revision: str = 'e98a777e272a'
down_revision: Union[str, Sequence[str], None] = '53625e49a6e5'
branch_labels = None
depends_on = None


categories = [
    ("Programming", "Software development and coding"),
    ("Design", "UI/UX and graphic design"),
    ("Business", "Entrepreneurship and management"),
    ("Marketing", "Digital and content marketing"),
    ("Data Science", "Data analysis and machine learning"),
    ("DevOps", "CI/CD, cloud and infrastructure"),
    ("Mobile Development", "iOS and Android development"),
    ("Cybersecurity", "Security and ethical hacking"),
]


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "categories",
            sa.column("id", sa.UUID(as_uuid=True)),
            sa.column("name", sa.String),
            sa.column("description", sa.String),
            sa.column("is_active", sa.Boolean),
        ),
        [
            {
                "id": uuid.uuid4(),
                "name": name,
                "description": desc,
                "is_active": True,
            }
            for name, desc in categories
        ]
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM categories WHERE name IN :names")
        .bindparams(names=[c[0] for c in categories])
    )