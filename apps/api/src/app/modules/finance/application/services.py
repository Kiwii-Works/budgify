"""Application services for finance module."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.modules.finance.domain.entities import Account, AccountCategory, Transaction, BudgetMonth, BudgetAllocation, WalletAccount
from app.modules.finance.infrastructure.repositories import SQLAlchemyWalletAccountRepository
# ──────────────── Wallet Accounts ────────────────
class WalletAccountService:
    def __init__(self, repo: SQLAlchemyWalletAccountRepository):
        self.repo = repo

    def create_wallet_account(self, wallet_account: WalletAccount) -> WalletAccount:
        return self.repo.create(wallet_account)

    def get_wallet_account(self, wallet_account_id: UUID, tenant_id: UUID) -> WalletAccount | None:
        return self.repo.get_by_id(wallet_account_id, tenant_id)

    def list_wallet_accounts(self, tenant_id: UUID, page: int, page_size: int) -> tuple[list[WalletAccount], int]:
        return self.repo.list(tenant_id, page, page_size)

    def update_wallet_account(self, wallet_account: WalletAccount) -> WalletAccount:
        return self.repo.update(wallet_account)

    def deactivate_wallet_account(self, wallet_account_id: UUID, tenant_id: UUID) -> None:
        self.repo.soft_delete(wallet_account_id, tenant_id)
from app.modules.finance.domain.exceptions import (
    AccountAlreadyExistsError,
    AccountCategoryAlreadyExistsError,
    AccountCategoryNotFoundError,
    AccountInactiveError,
    AccountNotFoundError,
    TransactionNotFoundError,
)
from app.modules.finance.domain.interfaces import (
    AccountCategoryRepository,
    AccountRepository,
    TransactionRepository,
    BudgetMonthRepository,
    BudgetAllocationRepository,
)
from app.modules.identity.domain.interfaces import AuditRepository


def _now() -> tuple[datetime, datetime]:
    """Return (naive_utc, aware_utc) timestamps."""
    now = datetime.now(UTC)
    return now.replace(tzinfo=None), now


def _snapshot(entity: AccountCategory | Account | Transaction) -> dict:
    """Build a JSONB-safe snapshot from an entity (excludes sensitive fields)."""
    result = {}
    for key, value in entity.__dict__.items():
        if key.startswith("_"):
            continue
        if isinstance(value, UUID):
            result[key] = str(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = str(value)
        elif hasattr(value, "isoformat"):  # date
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


# ── Account Category Services ─────────────────────────────────────────────────

class CreateCategoryService:
    def __init__(self, category_repo: AccountCategoryRepository, audit_repo: AuditRepository):
        self.category_repo = category_repo
        self.audit_repo = audit_repo

    def execute(self, tenant_id: UUID, name: str, description: str | None, user_id: UUID) -> AccountCategory:
        if self.category_repo.get_by_name(name, tenant_id):
            raise AccountCategoryAlreadyExistsError(f"Category '{name}' already exists in this tenant")

        naive, aware = _now()
        transaction_uid = uuid4()
        category = AccountCategory(
            category_id=uuid4(),
            tenant_id=tenant_id,
            name=name,
            description=description,
            is_active=True,
            created_by=user_id,
            modified_by=user_id,
            created_date=naive,
            created_date_utc=aware,
            modified_date=None,
            modified_date_utc=None,
        )
        category.transaction_uid = transaction_uid  # type: ignore[attr-defined]

        created = self.category_repo.create(category)

        self.audit_repo.log_transaction(transaction_uid, "CreateAccountCategory", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "CreateAccountCategory", "account_categories",
            created.category_id, "ADDED", tenant_id,
            changes={"before": None, "after": _snapshot(created)},
        )
        return created


class UpdateCategoryService:
    def __init__(self, category_repo: AccountCategoryRepository, audit_repo: AuditRepository):
        self.category_repo = category_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        category_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        name: str | None,
        description: str | None,
        is_active: bool | None,
    ) -> AccountCategory:
        category = self.category_repo.get_by_id(category_id, tenant_id)
        if not category:
            raise AccountCategoryNotFoundError()

        before = {}
        if name is not None and name != category.name:
            existing = self.category_repo.get_by_name(name, tenant_id)
            if existing and existing.category_id != category_id:
                raise AccountCategoryAlreadyExistsError(f"Category '{name}' already exists")
            before["name"] = category.name
            category.name = name
        if description is not None:
            before["description"] = category.description
            category.description = description
        if is_active is not None:
            before["is_active"] = category.is_active
            category.is_active = is_active

        naive, aware = _now()
        category.modified_by = user_id
        category.modified_date = naive
        category.modified_date_utc = aware
        transaction_uid = uuid4()
        category.transaction_uid = transaction_uid  # type: ignore[attr-defined]

        after = {k: getattr(category, k) for k in before}
        updated = self.category_repo.update(category)

        self.audit_repo.log_transaction(transaction_uid, "UpdateAccountCategory", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "UpdateAccountCategory", "account_categories",
            category_id, "MODIFIED", tenant_id,
            changes={"before": before, "after": after},
        )
        return updated


# ── Account Services ──────────────────────────────────────────────────────────

class CreateAccountService:
    def __init__(
        self,
        account_repo: AccountRepository,
        category_repo: AccountCategoryRepository,
        audit_repo: AuditRepository,
    ):
        self.account_repo = account_repo
        self.category_repo = category_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        tenant_id: UUID,
        category_id: UUID,
        name: str,
        description: str | None,
        type: str,
        user_id: UUID,
    ) -> Account:
        if not self.category_repo.get_by_id(category_id, tenant_id):
            raise AccountCategoryNotFoundError()
        if self.account_repo.get_by_name_and_type(name, type, tenant_id):
            raise AccountAlreadyExistsError(f"Account '{name}' of type '{type}' already exists")

        naive, aware = _now()
        transaction_uid = uuid4()
        account = Account(
            account_id=uuid4(),
            tenant_id=tenant_id,
            category_id=category_id,
            name=name,
            description=description,
            type=type,
            is_active=True,
            created_by=user_id,
            modified_by=user_id,
            created_date=naive,
            created_date_utc=aware,
            modified_date=None,
            modified_date_utc=None,
        )
        account.transaction_uid = transaction_uid  # type: ignore[attr-defined]

        created = self.account_repo.create(account)

        self.audit_repo.log_transaction(transaction_uid, "CreateAccount", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "CreateAccount", "accounts",
            created.account_id, "ADDED", tenant_id,
            changes={"before": None, "after": _snapshot(created)},
        )
        return created


class UpdateAccountService:
    def __init__(
        self,
        account_repo: AccountRepository,
        category_repo: AccountCategoryRepository,
        audit_repo: AuditRepository,
    ):
        self.account_repo = account_repo
        self.category_repo = category_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        account_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        category_id: UUID | None,
        name: str | None,
        description: str | None,
        is_active: bool | None,
    ) -> Account:
        account = self.account_repo.get_by_id(account_id, tenant_id)
        if not account:
            raise AccountNotFoundError()

        before = {}
        if category_id is not None and category_id != account.category_id:
            if not self.category_repo.get_by_id(category_id, tenant_id):
                raise AccountCategoryNotFoundError()
            before["category_id"] = str(account.category_id)
            account.category_id = category_id
        if name is not None and name != account.name:
            existing = self.account_repo.get_by_name_and_type(name, account.type, tenant_id)
            if existing and existing.account_id != account_id:
                raise AccountAlreadyExistsError(f"Account '{name}' already exists")
            before["name"] = account.name
            account.name = name
        if description is not None:
            before["description"] = account.description
            account.description = description
        if is_active is not None:
            before["is_active"] = account.is_active
            account.is_active = is_active

        naive, aware = _now()
        account.modified_by = user_id
        account.modified_date = naive
        account.modified_date_utc = aware
        transaction_uid = uuid4()
        account.transaction_uid = transaction_uid  # type: ignore[attr-defined]

        after = {k: str(getattr(account, k)) if isinstance(getattr(account, k), UUID) else getattr(account, k) for k in before}
        updated = self.account_repo.update(account)

        self.audit_repo.log_transaction(transaction_uid, "UpdateAccount", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "UpdateAccount", "accounts",
            account_id, "MODIFIED", tenant_id,
            changes={"before": before, "after": after},
        )
        return updated


# ── Transaction Services ──────────────────────────────────────────────────────

class CreateTransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        account_repo: AccountRepository,
        audit_repo: AuditRepository,
    ):
        self.transaction_repo = transaction_repo
        self.account_repo = account_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        tenant_id: UUID,
        account_id: UUID,
        amount: Decimal,
        currency: str,
        occurred_on,
        notes: str | None,
        direction: str,
        user_id: UUID,
    ) -> Transaction:
        account = self.account_repo.get_by_id(account_id, tenant_id)
        if not account:
            raise AccountNotFoundError()
        if not account.is_active:
            raise AccountInactiveError()

        naive, aware = _now()
        transaction_uid = uuid4()
        txn = Transaction(
            transaction_id=uuid4(),
            tenant_id=tenant_id,
            account_id=account_id,
            amount=amount,
            currency=currency,
            occurred_on=occurred_on,
            notes=notes,
            direction=direction,
            created_by=user_id,
            modified_by=user_id,
            created_date=naive,
            created_date_utc=aware,
            modified_date=None,
            modified_date_utc=None,
        )
        txn.transaction_uid = transaction_uid  # type: ignore[attr-defined]

        created = self.transaction_repo.create(txn)

        self.audit_repo.log_transaction(transaction_uid, "CreateTransaction", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "CreateTransaction", "transactions",
            created.transaction_id, "ADDED", tenant_id,
            changes={"before": None, "after": _snapshot(created)},
        )
        return created


class UpdateTransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        account_repo: AccountRepository,
        audit_repo: AuditRepository,
    ):
        self.transaction_repo = transaction_repo
        self.account_repo = account_repo
        self.audit_repo = audit_repo

    def execute(
        self,
        transaction_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        account_id: UUID | None,
        amount: Decimal | None,
        currency: str | None,
        occurred_on=None,
        notes: str | None = None,
        direction: str | None = None,
    ) -> Transaction:
        txn = self.transaction_repo.get_by_id(transaction_id, tenant_id)
        if not txn:
            raise TransactionNotFoundError()

        before = {}
        if account_id is not None and account_id != txn.account_id:
            account = self.account_repo.get_by_id(account_id, tenant_id)
            if not account:
                raise AccountNotFoundError()
            if not account.is_active:
                raise AccountInactiveError()
            before["account_id"] = str(txn.account_id)
            txn.account_id = account_id
        if amount is not None:
            before["amount"] = str(txn.amount)
            txn.amount = amount
        if currency is not None:
            before["currency"] = txn.currency
            txn.currency = currency
        if occurred_on is not None:
            before["occurred_on"] = txn.occurred_on.isoformat()
            txn.occurred_on = occurred_on
        if notes is not None:
            before["notes"] = txn.notes
            txn.notes = notes
        if direction is not None:
            before["direction"] = txn.direction
            txn.direction = direction

        naive, aware = _now()
        txn.modified_by = user_id
        txn.modified_date = naive
        txn.modified_date_utc = aware
        transaction_uid = uuid4()
        txn.transaction_uid = transaction_uid  # type: ignore[attr-defined]

        after = {}
        for k in before:
            val = getattr(txn, k)
            after[k] = str(val) if isinstance(val, (UUID, Decimal)) or hasattr(val, "isoformat") else val

        updated = self.transaction_repo.update(txn)

        self.audit_repo.log_transaction(transaction_uid, "UpdateTransaction", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "UpdateTransaction", "transactions",
            transaction_id, "MODIFIED", tenant_id,
            changes={"before": before, "after": after},
        )
        return updated


class DeleteTransactionService:
    def __init__(self, transaction_repo: TransactionRepository, audit_repo: AuditRepository):
        self.transaction_repo = transaction_repo
        self.audit_repo = audit_repo

    def execute(self, transaction_id: UUID, tenant_id: UUID, user_id: UUID) -> None:
        txn = self.transaction_repo.get_by_id(transaction_id, tenant_id)
        if not txn:
            raise TransactionNotFoundError()

        transaction_uid = uuid4()
        snapshot = _snapshot(txn)

        self.transaction_repo.delete(transaction_id, tenant_id)

        self.audit_repo.log_transaction(transaction_uid, "DeleteTransaction", user_id, tenant_id)
        self.audit_repo.log_detail(
            transaction_uid, "DeleteTransaction", "transactions",
            transaction_id, "DELETED", tenant_id,
            changes={"before": snapshot, "after": None},
        )


# ── Budget Month Services ─────────────────────────────────────────────────────

class BudgetMonthService:
    """Service for managing budget months (create, get, close, update)."""
    def __init__(self, repo: BudgetMonthRepository, audit_repo: AuditRepository):
        self.repo = repo
        self.audit_repo = audit_repo

    def create_budget_month(self, tenant_id: UUID, month: datetime.date, user_id: UUID, currency: str = "CAD") -> BudgetMonth:
        now, now_utc = _now()
        # Check if already exists
        if self.repo.get_by_month(tenant_id, month):
            raise Exception("Budget month already exists")
        budget_month = BudgetMonth(
            budget_month_id=uuid4(),
            tenant_id=tenant_id,
            month=month,
            status="DRAFT",
            currency=currency,
            closed_at=None,
            created_by=user_id,
            modified_by=None,
            created_date=now,
            created_date_utc=now_utc,
            modified_date=None,
            modified_date_utc=None,
        )
        result = self.repo.create(budget_month)
        # TODO: audit log
        return result

    def get_budget_month(self, tenant_id: UUID, month: datetime.date) -> BudgetMonth | None:
        return self.repo.get_by_month(tenant_id, month)

    def close_budget_month(self, budget_month_id: UUID, tenant_id: UUID, user_id: UUID) -> BudgetMonth:
        now, now_utc = _now()
        budget = self.repo.get_by_id(budget_month_id, tenant_id)
        if not budget:
            raise Exception("Budget month not found")
        if budget.status == "CLOSED":
            raise Exception("Budget month already closed")
        budget.status = "CLOSED"
        budget.closed_at = now_utc
        budget.modified_by = user_id
        budget.modified_date = now
        budget.modified_date_utc = now_utc
        result = self.repo.update(budget)
        # TODO: audit log
        return result


# ── Budget Allocation Services ───────────────────────────────────────────────

class BudgetAllocationService:
    """Service for managing budget allocations (bulk update, list)."""
    def __init__(self, repo: BudgetAllocationRepository, audit_repo: AuditRepository):
        self.repo = repo
        self.audit_repo = audit_repo

    def bulk_update_allocations(self, budget_month_id: UUID, allocations: list[dict], user_id: UUID) -> list[BudgetAllocation]:
        now, now_utc = _now()
        updated = []
        for alloc in allocations:
            # Assume alloc has allocation_id or (budget_month_id, category_id)
            entity = self.repo.get_by_budget_and_category(budget_month_id, alloc["category_id"])
            if entity:
                entity.planned_amount = Decimal(alloc["planned_amount"])
                entity.modified_by = user_id
                entity.modified_date = now
                entity.modified_date_utc = now_utc
                updated.append(entity)
            else:
                new_alloc = BudgetAllocation(
                    allocation_id=uuid4(),
                    budget_month_id=budget_month_id,
                    category_id=alloc["category_id"],
                    planned_amount=Decimal(alloc["planned_amount"]),
                    created_by=user_id,
                    modified_by=None,
                    created_date=now,
                    created_date_utc=now_utc,
                    modified_date=None,
                    modified_date_utc=None,
                )
                updated.append(new_alloc)
        result = self.repo.bulk_update(updated)
        # TODO: audit log
        return result

    def list_allocations(self, budget_month_id: UUID) -> list[BudgetAllocation]:
        return self.repo.list_by_budget(budget_month_id)
