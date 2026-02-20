
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from decimal import Decimal
from uuid import UUID

class WalletAccountType(str, Enum):
    CASH = "CASH"
    BANK = "BANK"
    CREDIT = "CREDIT"
    SAVINGS = "SAVINGS"

class CreateWalletAccountRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: WalletAccountType
    currency: str = Field(default="CAD", min_length=3, max_length=3)
    opening_balance: Decimal = Field(default=0.00, ge=0)

class UpdateWalletAccountRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    type: WalletAccountType | None = None
    currency: str | None = Field(None, min_length=3, max_length=3)
    opening_balance: Decimal | None = Field(None, ge=0)
    is_active: bool | None = None

class WalletAccountResponse(BaseModel):
    wallet_account_id: str
    tenant_id: str
    name: str
    type: WalletAccountType
    currency: str
    opening_balance: Decimal
    is_active: bool
"""Pydantic DTOs for finance module (API boundary only)."""

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


# ── Budgets ─────────────────────────────────────────────────────────────────

class BudgetMonthCreateRequest(BaseModel):
    """Request body for creating a budget month."""
    month: date
    currency: str = "CAD"

class BudgetMonthResponse(BaseModel):
    """Response model for a budget month."""
    budget_month_id: str
    tenant_id: str
    month: date
    status: str
    currency: str
    closed_at: date | None

class BudgetAllocationRequest(BaseModel):
    """Request body for a budget allocation (bulk update)."""
    category_id: UUID
    planned_amount: Decimal

class BudgetAllocationResponse(BaseModel):
    """Response model for a budget allocation."""
    allocation_id: str
    budget_month_id: str
    category_id: str
    planned_amount: Decimal

class BudgetSummaryCategoryRow(BaseModel):
    """Summary row for a category in the budget summary."""
    category_id: str
    category_name: str
    planned_amount: Decimal | None
    actual_amount: Decimal
    remaining_amount: Decimal | None
    is_unbudgeted: bool
    is_overbudget: bool

class BudgetSummaryResponse(BaseModel):
    """Response model for the budget summary."""
    month: date
    categories: list[BudgetSummaryCategoryRow]
    total_income: Decimal
    total_expenses: Decimal
    net: Decimal
    budgeted_total: Decimal
    unbudgeted_total: Decimal
