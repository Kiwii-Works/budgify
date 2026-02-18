"""create core tables

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all core tables."""

    # Create tenants table
    op.execute("""
        CREATE TABLE tenants (
            tenant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            tenant_name TEXT UNIQUE NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_by UUID NULL,
            modified_by UUID NULL,
            created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_date_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified_date TIMESTAMP NULL,
            modified_date_utc TIMESTAMPTZ NULL,
            operation_type operation_type NOT NULL DEFAULT 'ADDED',
            transaction_uid UUID NULL
        );
    """)
    op.execute("CREATE INDEX idx_tenants_name ON tenants(tenant_name);")
    op.execute("CREATE INDEX idx_tenants_active ON tenants(is_active);")

    # Create users table
    op.execute("""
        CREATE TABLE users (
            user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            username TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_by UUID NULL,
            modified_by UUID NULL,
            created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_date_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified_date TIMESTAMP NULL,
            modified_date_utc TIMESTAMPTZ NULL,
            operation_type operation_type NOT NULL DEFAULT 'ADDED',
            transaction_uid UUID NULL
        );
    """)
    op.execute("CREATE UNIQUE INDEX idx_users_email_lower ON users(LOWER(email));")
    op.execute("CREATE UNIQUE INDEX idx_users_username_lower ON users(LOWER(username));")
    op.execute("CREATE INDEX idx_users_active ON users(is_active);")

    # Create user_tenants table
    op.execute("""
        CREATE TABLE user_tenants (
            user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
            tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
            is_default BOOLEAN NOT NULL DEFAULT FALSE,
            PRIMARY KEY (user_id, tenant_id),
            created_by UUID NULL,
            modified_by UUID NULL,
            created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_date_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified_date TIMESTAMP NULL,
            modified_date_utc TIMESTAMPTZ NULL,
            operation_type operation_type NOT NULL DEFAULT 'ADDED',
            transaction_uid UUID NULL
        );
    """)
    op.execute("CREATE INDEX idx_user_tenants_tenant ON user_tenants(tenant_id);")
    op.execute("CREATE INDEX idx_user_tenants_default ON user_tenants(user_id, is_default) WHERE is_default = TRUE;")

    # Create roles table
    op.execute("""
        CREATE TABLE roles (
            role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            role_name TEXT UNIQUE NOT NULL,
            created_by UUID NULL,
            modified_by UUID NULL,
            created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_date_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified_date TIMESTAMP NULL,
            modified_date_utc TIMESTAMPTZ NULL,
            operation_type operation_type NOT NULL DEFAULT 'ADDED',
            transaction_uid UUID NULL
        );
    """)
    op.execute("CREATE UNIQUE INDEX idx_roles_name_lower ON roles(LOWER(role_name));")

    # Create user_tenant_roles table
    op.execute("""
        CREATE TABLE user_tenant_roles (
            user_id UUID NOT NULL,
            tenant_id UUID NOT NULL,
            role_id UUID NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
            PRIMARY KEY (user_id, tenant_id, role_id),
            created_by UUID NULL,
            modified_by UUID NULL,
            created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_date_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified_date TIMESTAMP NULL,
            modified_date_utc TIMESTAMPTZ NULL,
            operation_type operation_type NOT NULL DEFAULT 'ADDED',
            transaction_uid UUID NULL,
            FOREIGN KEY (user_id, tenant_id) REFERENCES user_tenants(user_id, tenant_id) ON DELETE CASCADE
        );
    """)
    op.execute("CREATE INDEX idx_user_tenant_roles_user ON user_tenant_roles(user_id);")
    op.execute("CREATE INDEX idx_user_tenant_roles_role ON user_tenant_roles(role_id);")
    op.execute("CREATE INDEX idx_user_tenant_roles_tenant ON user_tenant_roles(tenant_id);")
    op.execute("CREATE INDEX idx_user_tenant_roles_user_tenant ON user_tenant_roles(user_id, tenant_id);")

    # Create password_reset_tokens table
    op.execute("""
        CREATE TABLE password_reset_tokens (
            uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
            code_hash TEXT NOT NULL,
            expires_at_utc TIMESTAMPTZ NOT NULL,
            used_at_utc TIMESTAMPTZ NULL,
            created_at_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            attempt_count INTEGER NOT NULL DEFAULT 0
        );
    """)
    op.execute("CREATE INDEX idx_password_reset_user_id ON password_reset_tokens(user_id);")
    op.execute("CREATE INDEX idx_password_reset_expires ON password_reset_tokens(expires_at_utc);")

    # Create transactions_log table
    op.execute("""
        CREATE TABLE transactions_log (
            transaction_uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            action_type TEXT NOT NULL,
            transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            transaction_date_utc TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            modified_by UUID NULL REFERENCES users(user_id),
            tenant_id UUID NULL REFERENCES tenants(tenant_id)
        );
    """)
    op.execute("CREATE INDEX idx_transactions_log_modified_by ON transactions_log(modified_by);")
    op.execute("CREATE INDEX idx_transactions_log_date_utc ON transactions_log(transaction_date_utc);")
    op.execute("CREATE INDEX idx_transactions_log_tenant ON transactions_log(tenant_id);")
    op.execute("CREATE INDEX idx_transactions_log_tenant_date ON transactions_log(tenant_id, transaction_date_utc);")

    # Create transaction_log_details table
    op.execute("""
        CREATE TABLE transaction_log_details (
            uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            transaction_uid UUID NOT NULL REFERENCES transactions_log(transaction_uid) ON DELETE CASCADE,
            action_type TEXT NOT NULL,
            entity_domain TEXT NOT NULL,
            entity_id UUID NULL,
            transaction_description operation_type NOT NULL,
            changes JSONB NULL,
            tenant_id UUID NULL REFERENCES tenants(tenant_id)
        );
    """)
    op.execute("CREATE INDEX idx_transaction_details_transaction_uid ON transaction_log_details(transaction_uid);")
    op.execute("CREATE INDEX idx_transaction_details_entity_id ON transaction_log_details(entity_id);")
    op.execute("CREATE INDEX idx_transaction_details_changes_jsonb ON transaction_log_details USING GIN(changes);")
    op.execute("CREATE INDEX idx_transaction_details_tenant ON transaction_log_details(tenant_id);")
    op.execute("CREATE INDEX idx_transaction_details_tenant_entity ON transaction_log_details(tenant_id, entity_domain, entity_id);")


def downgrade() -> None:
    """Drop all core tables in reverse order."""
    op.execute("DROP TABLE IF EXISTS transaction_log_details CASCADE;")
    op.execute("DROP TABLE IF EXISTS transactions_log CASCADE;")
    op.execute("DROP TABLE IF EXISTS password_reset_tokens CASCADE;")
    op.execute("DROP TABLE IF EXISTS user_tenant_roles CASCADE;")
    op.execute("DROP TABLE IF EXISTS roles CASCADE;")
    op.execute("DROP TABLE IF EXISTS user_tenants CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
    op.execute("DROP TABLE IF EXISTS tenants CASCADE;")
