"""Pydantic DTOs for finance module (API boundary only)."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


# ── Account Category ──────────────────────────────────────────────────────────

class CreateCategoryRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class UpdateCategoryRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    category_id: str
    tenant_id: str
    name: str
    description: str | None
    is_active: bool


# ── Account ───────────────────────────────────────────────────────────────────

class CreateAccountRequest(BaseModel):
    category_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    type: str = Field(..., pattern="^(INCOME|EXPENSE)$")


class UpdateAccountRequest(BaseModel):
    category_id: UUID | None = None
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    is_active: bool | None = None


class AccountResponse(BaseModel):
    account_id: str
    tenant_id: str
    category_id: str
    name: str
    description: str | None
    type: str
    is_active: bool


# ── Transaction ───────────────────────────────────────────────────────────────

class CreateTransactionRequest(BaseModel):
    account_id: UUID
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(default="CAD", min_length=3, max_length=3)
    occurred_on: date
    notes: str | None = None
    direction: str = Field(..., pattern="^(INCOME|EXPENSE)$")


class UpdateTransactionRequest(BaseModel):
    account_id: UUID | None = None
    amount: Decimal | None = Field(None, gt=0, decimal_places=2)
    currency: str | None = Field(None, min_length=3, max_length=3)
    occurred_on: date | None = None
    notes: str | None = None
    direction: str | None = Field(None, pattern="^(INCOME|EXPENSE)$")


class TransactionResponse(BaseModel):
    transaction_id: str
    tenant_id: str
    account_id: str
    amount: str  # serialized as string to avoid float precision issues
    currency: str
    occurred_on: str
    notes: str | None
    direction: str
