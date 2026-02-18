"""create extensions and enums

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create PostgreSQL extensions and enums."""
    # Enable pgcrypto for gen_random_uuid()
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    # Create operation_type enum (action_type is TEXT for flexibility)
    op.execute("""
        CREATE TYPE operation_type AS ENUM ('ADDED', 'MODIFIED', 'DELETED');
    """)


def downgrade() -> None:
    """Drop enums (extension not dropped as other databases might use it)."""
    op.execute("DROP TYPE IF EXISTS operation_type;")
    # Note: Don't drop pgcrypto as other databases might use it
