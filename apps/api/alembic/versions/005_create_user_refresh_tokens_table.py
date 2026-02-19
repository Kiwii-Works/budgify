"""Create user refresh tokens table.

Revision ID: 005
Revises: 004
Create Date: 2026-02-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade: Create user_refresh_tokens table."""
    op.create_table(
        'user_refresh_tokens',
        sa.Column('refresh_token_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('token_hash', sa.String(256), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        
        # Primary key constraint
        sa.PrimaryKeyConstraint('refresh_token_id'),
        
        # Foreign key constraints
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.tenant_id'], ondelete='CASCADE'),
    )
    
    # Create indexes for query performance
    op.create_index(
        'ix_user_refresh_tokens_user_tenant',
        'user_refresh_tokens',
        ['user_id', 'tenant_id'],
        unique=False
    )
    op.create_index(
        'ix_user_refresh_tokens_expires_at',
        'user_refresh_tokens',
        ['expires_at'],
        unique=False
    )
    op.create_index(
        'ix_user_refresh_tokens_token_hash',
        'user_refresh_tokens',
        ['token_hash'],
        unique=False
    )
    op.create_index(
        'ix_user_refresh_tokens_revoked_at_partial',
        'user_refresh_tokens',
        ['revoked_at'],
        postgresql_where=sa.text('revoked_at IS NULL'),
        unique=False
    )


def downgrade() -> None:
    """Downgrade: Drop user_refresh_tokens table."""
    op.drop_index('ix_user_refresh_tokens_revoked_at_partial', table_name='user_refresh_tokens')
    op.drop_index('ix_user_refresh_tokens_token_hash', table_name='user_refresh_tokens')
    op.drop_index('ix_user_refresh_tokens_expires_at', table_name='user_refresh_tokens')
    op.drop_index('ix_user_refresh_tokens_user_tenant', table_name='user_refresh_tokens')
    
    op.drop_table('user_refresh_tokens')
