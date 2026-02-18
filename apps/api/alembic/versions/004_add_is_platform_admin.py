"""add is_platform_admin to users

Revision ID: 004
Revises: 003
Create Date: 2024-01-01 00:00:03.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_platform_admin column to users table."""
    op.execute("""
        ALTER TABLE users
        ADD COLUMN is_platform_admin BOOLEAN NOT NULL DEFAULT FALSE;
    """)


def downgrade() -> None:
    """Remove is_platform_admin column from users table."""
    op.execute("ALTER TABLE users DROP COLUMN is_platform_admin;")
