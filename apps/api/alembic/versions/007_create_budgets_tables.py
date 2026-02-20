"""Create budget_months and budget_allocations tables

Revision ID: 007
Revises: 006
Create Date: 2026-02-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'budget_months',
        sa.Column('budget_month_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('month', sa.Date(), nullable=False),
        sa.Column('status', sa.Text(), nullable=False),
        sa.Column('currency', sa.Text(), nullable=False, server_default='CAD'),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        # Audit fields
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('modified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_date_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('modified_date', sa.DateTime(timezone=False), nullable=True),
        sa.Column('modified_date_utc', sa.DateTime(timezone=True), nullable=True),
        sa.Column('operation_type', sa.String(20), nullable=False, server_default='ADDED'),
        sa.Column('transaction_uid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('budget_month_id'),
        sa.UniqueConstraint('tenant_id', 'month', name='uq_budget_months_tenant_month'),
    )
    op.create_index('ix_budget_months_tenant_id_month', 'budget_months', ['tenant_id', 'month'])

    op.create_table(
        'budget_allocations',
        sa.Column('allocation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('budget_month_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('planned_amount', sa.Numeric(12, 2), nullable=False),
        # Audit fields
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('modified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_date_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('modified_date', sa.DateTime(timezone=False), nullable=True),
        sa.Column('modified_date_utc', sa.DateTime(timezone=True), nullable=True),
        sa.Column('operation_type', sa.String(20), nullable=False, server_default='ADDED'),
        sa.Column('transaction_uid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint('allocation_id'),
        sa.UniqueConstraint('budget_month_id', 'category_id', name='uq_budget_allocations_budget_month_category'),
        sa.ForeignKeyConstraint(['budget_month_id'], ['budget_months.budget_month_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['account_categories.category_id'], ondelete='CASCADE'),
        sa.CheckConstraint('planned_amount >= 0', name='ck_budget_allocations_planned_amount_nonnegative'),
    )
    op.create_index('ix_budget_allocations_budget_month_id_category_id', 'budget_allocations', ['budget_month_id', 'category_id'])

def downgrade() -> None:
    op.drop_index('ix_budget_allocations_budget_month_id_category_id', table_name='budget_allocations')
    op.drop_table('budget_allocations')
    op.drop_index('ix_budget_months_tenant_id_month', table_name='budget_months')
    op.drop_table('budget_months')