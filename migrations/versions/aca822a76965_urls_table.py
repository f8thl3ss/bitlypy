"""Create users table and short_urls table

Revision ID: aca822a76965
Revises: 
Create Date: 2024-01-06 16:02:12.965384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aca822a76965"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Uuid, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
    )
    op.create_table(
        "short_urls",
        sa.Column("short_url", sa.String, primary_key=True),
        sa.Column("original_url", sa.String, nullable=False),
        sa.Column(
            "owner_id",
            sa.String,
            sa.ForeignKey("users.user_id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("short_urls")
