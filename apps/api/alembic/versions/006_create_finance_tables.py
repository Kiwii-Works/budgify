"""Create finance tables.

Revision ID: 006
Revises: 005
Create Date: 2026-02-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade: Create account_categories, accounts, transactions tables."""

    # ── account_categories ────────────────────────────────────────────────────
    op.create_table(
        'account_categories',
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),

        # Audit fields
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('modified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_date_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('modified_date', sa.DateTime(timezone=False), nullable=True),
        sa.Column('modified_date_utc', sa.DateTime(timezone=True), nullable=True),
        sa.Column('operation_type', sa.String(20), nullable=False, server_default='ADDED'),
        sa.Column('transaction_uid', postgresql.UUID(as_uuid=True), nullable=True),

        sa.PrimaryKeyConstraint('category_id'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.tenant_id'], ondelete='CASCADE'),
        sa.CheckConstraint("length(trim(name)) > 0", name='ck_account_categories_name_nonempty'),
    )

    op.create_index('ix_account_categories_tenant_id', 'account_categories', ['tenant_id'])
    op.create_index('ix_account_categories_is_active', 'account_categories', ['is_active'])
    op.create_index(
        'uq_account_categories_tenant_name',
        'account_categories',
        [sa.text('tenant_id'), sa.text('lower(name)')],
        unique=True,
    )

    # ── accounts ──────────────────────────────────────────────────────────────
    op.create_table(
        'accounts',
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),

        # Audit fields
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('modified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_date_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('modified_date', sa.DateTime(timezone=False), nullable=True),
        sa.Column('modified_date_utc', sa.DateTime(timezone=True), nullable=True),
        sa.Column('operation_type', sa.String(20), nullable=False, server_default='ADDED'),
        sa.Column('transaction_uid', postgresql.UUID(as_uuid=True), nullable=True),

        sa.PrimaryKeyConstraint('account_id'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.tenant_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['account_categories.category_id'], ondelete='RESTRICT'),
        sa.CheckConstraint("type IN ('INCOME', 'EXPENSE')", name='ck_accounts_type'),
        sa.CheckConstraint("length(trim(name)) > 0", name='ck_accounts_name_nonempty'),
    )

    op.create_index('ix_accounts_tenant_id', 'accounts', ['tenant_id'])
    op.create_index('ix_accounts_category_id', 'accounts', ['category_id'])
    op.create_index('ix_accounts_is_active', 'accounts', ['is_active'])
    op.create_index(
        'uq_accounts_tenant_name_type',
        'accounts',
        [sa.text('tenant_id'), sa.text('lower(name)'), sa.text('type')],
        unique=True,
    )

    # ── transactions ──────────────────────────────────────────────────────────
    op.create_table(
        'transactions',
        sa.Column('transaction_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.Text(), nullable=False, server_default='CAD'),
        sa.Column('occurred_on', sa.Date(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('direction', sa.Text(), nullable=False),

        # Audit fields
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('modified_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_date_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('modified_date', sa.DateTime(timezone=False), nullable=True),
        sa.Column('modified_date_utc', sa.DateTime(timezone=True), nullable=True),
        sa.Column('operation_type', sa.String(20), nullable=False, server_default='ADDED'),
        sa.Column('transaction_uid', postgresql.UUID(as_uuid=True), nullable=True),

        sa.PrimaryKeyConstraint('transaction_id'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.tenant_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.account_id'], ondelete='RESTRICT'),
        sa.CheckConstraint("amount > 0", name='ck_transactions_amount_positive'),
        sa.CheckConstraint("direction IN ('INCOME', 'EXPENSE')", name='ck_transactions_direction'),
    )

    op.create_index('ix_transactions_tenant_id', 'transactions', ['tenant_id'])
    op.create_index('ix_transactions_account_id', 'transactions', ['account_id'])
    op.create_index('ix_transactions_occurred_on', 'transactions', ['occurred_on'])
    op.create_index('ix_transactions_direction', 'transactions', ['direction'])


def downgrade() -> None:
    """Downgrade: Drop finance tables in reverse dependency order."""
    op.drop_index('ix_transactions_direction', table_name='transactions')
    op.drop_index('ix_transactions_occurred_on', table_name='transactions')
    op.drop_index('ix_transactions_account_id', table_name='transactions')
    op.drop_index('ix_transactions_tenant_id', table_name='transactions')
    op.drop_table('transactions')

    op.drop_index('uq_accounts_tenant_name_type', table_name='accounts')
    op.drop_index('ix_accounts_is_active', table_name='accounts')
    op.drop_index('ix_accounts_category_id', table_name='accounts')
    op.drop_index('ix_accounts_tenant_id', table_name='accounts')
    op.drop_table('accounts')

    op.drop_index('uq_account_categories_tenant_name', table_name='account_categories')
    op.drop_index('ix_account_categories_is_active', table_name='account_categories')
    op.drop_index('ix_account_categories_tenant_id', table_name='account_categories')
    op.drop_table('account_categories')
