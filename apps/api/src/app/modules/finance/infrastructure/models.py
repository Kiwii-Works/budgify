"""SQLAlchemy ORM models for finance module."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, Column, Date, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SQLEnum

from app.core.database import Base
from app.modules.identity.infrastructure.models import OperationType


class AccountCategory(Base):
    """Account category ORM model."""

    __tablename__ = "account_categories"

    category_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
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

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="ck_account_categories_name_nonempty"),
    )


class Account(Base):
    """Account ORM model."""

    __tablename__ = "accounts"

    account_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(PGUUID(as_uuid=True), ForeignKey("account_categories.category_id", ondelete="RESTRICT"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Text, nullable=False)
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

    __table_args__ = (
        CheckConstraint("type IN ('INCOME', 'EXPENSE')", name="ck_accounts_type"),
        CheckConstraint("length(trim(name)) > 0", name="ck_accounts_name_nonempty"),
    )


class FinancialTransaction(Base):
    """Financial transaction ORM model."""

    __tablename__ = "transactions"

    transaction_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PGUUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    account_id = Column(PGUUID(as_uuid=True), ForeignKey("accounts.account_id", ondelete="RESTRICT"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(Text, nullable=False, default="CAD")
    occurred_on = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    direction = Column(Text, nullable=False)

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

    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),
        CheckConstraint("direction IN ('INCOME', 'EXPENSE')", name="ck_transactions_direction"),
    )
