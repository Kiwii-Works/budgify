"""seed roles

Revision ID: 003
Revises: 002
Create Date: 2024-01-01 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed initial roles."""
    conn = op.get_bind()

    roles = ['SUDO', 'READER', 'EDITOR', 'REPORTER']

    for role_name in roles:
        conn.execute(
            text("""
                INSERT INTO roles (role_id, role_name, created_date, created_date_utc, operation_type)
                VALUES (gen_random_uuid(), :role_name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'ADDED')
            """),
            {"role_name": role_name}
        )


def downgrade() -> None:
    """Remove seeded roles."""
    conn = op.get_bind()
    conn.execute(
        text("DELETE FROM roles WHERE role_name IN ('SUDO', 'READER', 'EDITOR', 'REPORTER')")
    )
