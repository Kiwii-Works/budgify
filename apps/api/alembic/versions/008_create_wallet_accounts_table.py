"""
Revision ID: 008_create_wallet_accounts_table
Revises: 007
Create Date: 2024-05-01

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '008_create_wallet_accounts_table'
down_revision = '007'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'wallet_accounts',
        sa.Column('wallet_account_id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', pg.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.Enum('CASH', 'BANK', 'CREDIT', 'SAVINGS', name='walletaccounttype'), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='CAD'),
        sa.Column('opening_balance', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )

def downgrade():
    op.drop_table('wallet_accounts')
    op.execute("DROP TYPE IF EXISTS walletaccounttype")
