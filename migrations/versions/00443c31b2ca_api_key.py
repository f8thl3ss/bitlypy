"""Create api keys table

Revision ID: 00443c31b2ca
Revises: aca822a76965
Create Date: 2024-01-07 11:23:20.667682

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "00443c31b2ca"
down_revision = "aca822a76965"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "api_keys",
        sa.Column("key", sa.String(32), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid, sa.ForeignKey("users.user_id", ondelete="CASCADE")
        ),
    )


def downgrade():
    op.drop_table("api_keys")
