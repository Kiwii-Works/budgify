"""Finance domain entities (plain Python, no framework dependencies)."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class AccountCategory:
    """Account category domain entity."""

    category_id: UUID
    tenant_id: UUID
    name: str
    description: str | None
    is_active: bool
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None


@dataclass
class Account:
    """Account domain entity."""

    account_id: UUID
    tenant_id: UUID
    category_id: UUID
    name: str
    description: str | None
    type: str  # INCOME | EXPENSE
    is_active: bool
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None


@dataclass
class Transaction:
    """Financial transaction domain entity."""

    transaction_id: UUID
    tenant_id: UUID
    account_id: UUID
    amount: Decimal
    currency: str
    occurred_on: date
    notes: str | None
    direction: str  # INCOME | EXPENSE
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None
