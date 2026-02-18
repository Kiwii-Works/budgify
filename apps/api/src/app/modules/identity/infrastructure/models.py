"""SQLAlchemy ORM models for identity module."""

# PostgreSQL Enum for operation_type (ADDED, MODIFIED, DELETED)
import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    text,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.core.database import Base


class OperationType(enum.Enum):
    """Operation type enum for audit fields."""

    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"


# Tenant Model
class Tenant(Base):
    """Tenant ORM model."""

    __tablename__ = "tenants"

    tenant_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_name = Column(Text, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Audit fields
    created_by = Column(PGUUID(as_uuid=True), nullable=True)
    modified_by = Column(PGUUID(as_uuid=True), nullable=True)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow)
    created_date_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified_date = Column(TIMESTAMP(timezone=False), nullable=True)
    modified_date_utc = Column(TIMESTAMP(timezone=True), nullable=True)
    operation_type = Column(
        SQLEnum(OperationType, native_enum=False, create_constraint=True),
        nullable=False,
        default=OperationType.ADDED,
    )
    transaction_uid = Column(PGUUID(as_uuid=True), nullable=True)

    # Indexes
    __table_args__ = (
        Index("idx_tenants_name", "tenant_name"),
        Index("idx_tenants_active", "is_active"),
    )


# User Model (Global - no tenant_id)
class User(Base):
    """User ORM model (global identity)."""

    __tablename__ = "users"

    user_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(Text, unique=True, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    phone_number = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_platform_admin = Column(Boolean, nullable=False, default=False)

    # Audit fields
    created_by = Column(PGUUID(as_uuid=True), nullable=True)
    modified_by = Column(PGUUID(as_uuid=True), nullable=True)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow)
    created_date_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified_date = Column(TIMESTAMP(timezone=False), nullable=True)
    modified_date_utc = Column(TIMESTAMP(timezone=True), nullable=True)
    operation_type = Column(
        SQLEnum(OperationType, native_enum=False, create_constraint=True),
        nullable=False,
        default=OperationType.ADDED,
    )
    transaction_uid = Column(PGUUID(as_uuid=True), nullable=True)

    # Indexes
    __table_args__ = (
        Index("idx_users_email_lower", text("LOWER(email)"), unique=True),
        Index("idx_users_username_lower", text("LOWER(username)"), unique=True),
        Index("idx_users_active", "is_active"),
    )


# UserTenant Model (Membership Table)
class UserTenant(Base):
    """User-Tenant membership ORM model."""

    __tablename__ = "user_tenants"

    user_id = Column(
        PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True
    )
    tenant_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
        primary_key=True,
    )
    is_default = Column(Boolean, nullable=False, default=False)

    # Audit fields
    created_by = Column(PGUUID(as_uuid=True), nullable=True)
    modified_by = Column(PGUUID(as_uuid=True), nullable=True)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow)
    created_date_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified_date = Column(TIMESTAMP(timezone=False), nullable=True)
    modified_date_utc = Column(TIMESTAMP(timezone=True), nullable=True)
    operation_type = Column(
        SQLEnum(OperationType, native_enum=False, create_constraint=True),
        nullable=False,
        default=OperationType.ADDED,
    )
    transaction_uid = Column(PGUUID(as_uuid=True), nullable=True)

    # Indexes
    __table_args__ = (
        Index("idx_user_tenants_tenant", "tenant_id"),
        Index(
            "idx_user_tenants_default",
            "user_id",
            "is_default",
            postgresql_where=text("is_default = TRUE"),
        ),
    )


# Role Model (Global Definitions)
class Role(Base):
    """Role ORM model (global role definitions)."""

    __tablename__ = "roles"

    role_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    role_name = Column(Text, unique=True, nullable=False)

    # Audit fields
    created_by = Column(PGUUID(as_uuid=True), nullable=True)
    modified_by = Column(PGUUID(as_uuid=True), nullable=True)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow)
    created_date_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified_date = Column(TIMESTAMP(timezone=False), nullable=True)
    modified_date_utc = Column(TIMESTAMP(timezone=True), nullable=True)
    operation_type = Column(
        SQLEnum(OperationType, native_enum=False, create_constraint=True),
        nullable=False,
        default=OperationType.ADDED,
    )
    transaction_uid = Column(PGUUID(as_uuid=True), nullable=True)

    # Indexes
    __table_args__ = (Index("idx_roles_name_lower", text("LOWER(role_name)"), unique=True),)


# UserTenantRole Model (Tenant-Scoped Role Assignments)
class UserTenantRole(Base):
    """User-Tenant-Role assignment ORM model."""

    __tablename__ = "user_tenant_roles"

    user_id = Column(PGUUID(as_uuid=True), primary_key=True)
    tenant_id = Column(PGUUID(as_uuid=True), primary_key=True)
    role_id = Column(
        PGUUID(as_uuid=True), ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True
    )

    # Audit fields
    created_by = Column(PGUUID(as_uuid=True), nullable=True)
    modified_by = Column(PGUUID(as_uuid=True), nullable=True)
    created_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow)
    created_date_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified_date = Column(TIMESTAMP(timezone=False), nullable=True)
    modified_date_utc = Column(TIMESTAMP(timezone=True), nullable=True)
    operation_type = Column(
        SQLEnum(OperationType, native_enum=False, create_constraint=True),
        nullable=False,
        default=OperationType.ADDED,
    )
    transaction_uid = Column(PGUUID(as_uuid=True), nullable=True)

    # Foreign key constraint to user_tenants
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "tenant_id"],
            ["user_tenants.user_id", "user_tenants.tenant_id"],
            ondelete="CASCADE",
        ),
        Index("idx_user_tenant_roles_user", "user_id"),
        Index("idx_user_tenant_roles_role", "role_id"),
        Index("idx_user_tenant_roles_tenant", "tenant_id"),
        Index("idx_user_tenant_roles_user_tenant", "user_id", "tenant_id"),
    )


# PasswordResetToken Model
class PasswordResetToken(Base):
    """Password reset token ORM model."""

    __tablename__ = "password_reset_tokens"

    uid = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    code_hash = Column(Text, nullable=False)
    expires_at_utc = Column(TIMESTAMP(timezone=True), nullable=False)
    used_at_utc = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    attempt_count = Column(Integer, nullable=False, default=0)

    # Indexes
    __table_args__ = (
        Index("idx_password_reset_user_id", "user_id"),
        Index("idx_password_reset_expires", "expires_at_utc"),
    )


# TransactionsLog Model (Audit Master)
class TransactionsLog(Base):
    """Transactions log ORM model (audit master)."""

    __tablename__ = "transactions_log"

    transaction_uid = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    action_type = Column(Text, nullable=False)  # TEXT for flexibility
    transaction_date = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow)
    transaction_date_utc = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified_by = Column(PGUUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=True)

    # Indexes
    __table_args__ = (
        Index("idx_transactions_log_modified_by", "modified_by"),
        Index("idx_transactions_log_date_utc", "transaction_date_utc"),
        Index("idx_transactions_log_tenant", "tenant_id"),
        Index("idx_transactions_log_tenant_date", "tenant_id", "transaction_date_utc"),
    )


# TransactionLogDetails Model
class TransactionLogDetails(Base):
    """Transaction log details ORM model."""

    __tablename__ = "transaction_log_details"

    uid = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    transaction_uid = Column(
        PGUUID(as_uuid=True),
        ForeignKey("transactions_log.transaction_uid", ondelete="CASCADE"),
        nullable=False,
    )
    action_type = Column(Text, nullable=False)  # TEXT for flexibility
    entity_domain = Column(Text, nullable=False)
    entity_id = Column(PGUUID(as_uuid=True), nullable=True)
    transaction_description = Column(
        SQLEnum(OperationType, native_enum=False, create_constraint=True),
        nullable=False,
    )
    changes = Column(JSONB, nullable=True)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=True)

    # Indexes
    __table_args__ = (
        Index("idx_transaction_details_transaction_uid", "transaction_uid"),
        Index("idx_transaction_details_entity_id", "entity_id"),
        Index("idx_transaction_details_changes_jsonb", "changes", postgresql_using="gin"),
        Index("idx_transaction_details_tenant", "tenant_id"),
        Index("idx_transaction_details_tenant_entity", "tenant_id", "entity_domain", "entity_id"),
    )
