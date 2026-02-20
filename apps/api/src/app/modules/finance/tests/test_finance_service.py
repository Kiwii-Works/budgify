"""Unit tests for finance application services."""

from datetime import date, datetime, UTC
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.modules.finance.application.services import (
    BudgetMonthService,
    BudgetAllocationService,
    CreateAccountService,
    CreateCategoryService,
    CreateTransactionService,
    DeleteTransactionService,
    UpdateAccountService,
    UpdateCategoryService,
    UpdateTransactionService,
    WalletAccountService,
)
from app.modules.finance.domain.entities import Account, AccountCategory, BudgetMonth, BudgetAllocation, Transaction, WalletAccount
# ── WalletAccount Helper ─────────────────────────────────────────────────────
def _make_wallet_account(**kwargs) -> WalletAccount:
    defaults = dict(
        wallet_account_id=uuid4(),
        tenant_id=uuid4(),
        name="Main Wallet",
        type="CASH",
        currency="CAD",
        opening_balance=Decimal("100.00"),
        is_active=True,
    )
    defaults.update(kwargs)
    return WalletAccount(**defaults)


# ── WalletAccountService Tests ───────────────────────────────────────────────
class TestWalletAccountService:
    def test_create_wallet_account(self):
        repo = MagicMock()
        wallet = _make_wallet_account()
        repo.create.return_value = wallet
        service = WalletAccountService(repo)
        result = service.create_wallet_account(wallet)
        assert result == wallet

    def test_get_wallet_account(self):
        repo = MagicMock()
        wallet = _make_wallet_account()
        repo.get_by_id.return_value = wallet
        service = WalletAccountService(repo)
        result = service.get_wallet_account(wallet.wallet_account_id, wallet.tenant_id)
        assert result == wallet

    def test_list_wallet_accounts(self):
        repo = MagicMock()
        wallet = _make_wallet_account()
        repo.list.return_value = ([wallet], 1)
        service = WalletAccountService(repo)
        items, total = service.list_wallet_accounts(wallet.tenant_id, 1, 10)
        assert items == [wallet]
        assert total == 1

    def test_update_wallet_account(self):
        repo = MagicMock()
        wallet = _make_wallet_account()
        repo.update.return_value = wallet
        service = WalletAccountService(repo)
        result = service.update_wallet_account(wallet)
        assert result == wallet

    def test_deactivate_wallet_account(self):
        repo = MagicMock()
        service = WalletAccountService(repo)
        wallet_id = uuid4()
        tenant_id = uuid4()
        service.deactivate_wallet_account(wallet_id, tenant_id)
        repo.soft_delete.assert_called_once_with(wallet_id, tenant_id)
from app.modules.finance.domain.exceptions import (
    AccountAlreadyExistsError,
    AccountCategoryAlreadyExistsError,
    AccountCategoryNotFoundError,
    AccountInactiveError,
    AccountNotFoundError,
    TransactionNotFoundError,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_category(**kwargs) -> AccountCategory:
    now = datetime.now(UTC)
    defaults = dict(
        category_id=uuid4(),
        tenant_id=uuid4(),
        name="Food",
        description=None,
        is_active=True,
        created_by=uuid4(),
        modified_by=uuid4(),
        created_date=now.replace(tzinfo=None),
        created_date_utc=now,
        modified_date=None,
        modified_date_utc=None,
    )
    defaults.update(kwargs)
    return AccountCategory(**defaults)


def _make_account(**kwargs) -> Account:
    now = datetime.now(UTC)
    defaults = dict(
        account_id=uuid4(),
        tenant_id=uuid4(),
        category_id=uuid4(),
        name="Salary",
        description=None,
        type="INCOME",
        is_active=True,
        created_by=uuid4(),
        modified_by=uuid4(),
        created_date=now.replace(tzinfo=None),
        created_date_utc=now,
        modified_date=None,
        modified_date_utc=None,
    )
    defaults.update(kwargs)
    return Account(**defaults)


def _make_transaction(**kwargs) -> Transaction:
    now = datetime.now(UTC)
    defaults = dict(
        transaction_id=uuid4(),
        tenant_id=uuid4(),
        account_id=uuid4(),
        amount=Decimal("100.00"),
        currency="CAD",
        occurred_on=date.today(),
        notes=None,
        direction="INCOME",
        created_by=uuid4(),
        modified_by=uuid4(),
        created_date=now.replace(tzinfo=None),
        created_date_utc=now,
        modified_date=None,
        modified_date_utc=None,
    )
    defaults.update(kwargs)
    return Transaction(**defaults)


def _make_budget_month(**kwargs) -> BudgetMonth:
    now = datetime.now(UTC)
    defaults = dict(
        budget_month_id=uuid4(),
        tenant_id=uuid4(),
        month=date(2025, 2, 1),
        status="DRAFT",
        currency="CAD",
        closed_at=None,
        created_by=uuid4(),
        modified_by=None,
        created_date=now.replace(tzinfo=None),
        created_date_utc=now,
        modified_date=None,
        modified_date_utc=None,
    )
    defaults.update(kwargs)
    return BudgetMonth(**defaults)


def _mock_audit() -> MagicMock:
    audit = MagicMock()
    audit.log_transaction = MagicMock()
    audit.log_detail = MagicMock()
    return audit


# ── CreateCategoryService ─────────────────────────────────────────────────────

class TestCreateCategoryService:
    def test_creates_category_successfully(self):
        tenant_id = uuid4()
        user_id = uuid4()
        category_repo = MagicMock()
        category_repo.get_by_name.return_value = None
        created = _make_category(tenant_id=tenant_id, name="Food")
        category_repo.create.return_value = created

        audit = _mock_audit()
        service = CreateCategoryService(category_repo, audit)
        result = service.execute(tenant_id, "Food", None, user_id)

        assert result.name == "Food"
        category_repo.create.assert_called_once()
        audit.log_transaction.assert_called_once()
        audit.log_detail.assert_called_once()

    def test_raises_if_name_already_exists(self):
        tenant_id = uuid4()
        user_id = uuid4()
        category_repo = MagicMock()
        category_repo.get_by_name.return_value = _make_category(name="Food")

        service = CreateCategoryService(category_repo, _mock_audit())
        with pytest.raises(AccountCategoryAlreadyExistsError):
            service.execute(tenant_id, "Food", None, user_id)


# ── UpdateCategoryService ─────────────────────────────────────────────────────

class TestUpdateCategoryService:
    def test_updates_name_successfully(self):
        tenant_id = uuid4()
        user_id = uuid4()
        category = _make_category(tenant_id=tenant_id, name="Food")

        category_repo = MagicMock()
        category_repo.get_by_id.return_value = category
        category_repo.get_by_name.return_value = None
        updated = _make_category(
            category_id=category.category_id,
            tenant_id=tenant_id,
            name="Groceries",
        )
        category_repo.update.return_value = updated

        service = UpdateCategoryService(category_repo, _mock_audit())
        result = service.execute(category.category_id, tenant_id, user_id, "Groceries", None, None)

        assert result.name == "Groceries"

    def test_raises_if_category_not_found(self):
        category_repo = MagicMock()
        category_repo.get_by_id.return_value = None

        service = UpdateCategoryService(category_repo, _mock_audit())
        with pytest.raises(AccountCategoryNotFoundError):
            service.execute(uuid4(), uuid4(), uuid4(), "X", None, None)

    def test_raises_if_new_name_conflicts(self):
        tenant_id = uuid4()
        category = _make_category(tenant_id=tenant_id, name="Food")
        other = _make_category(tenant_id=tenant_id, name="Groceries")

        category_repo = MagicMock()
        category_repo.get_by_id.return_value = category
        category_repo.get_by_name.return_value = other

        service = UpdateCategoryService(category_repo, _mock_audit())
        with pytest.raises(AccountCategoryAlreadyExistsError):
            service.execute(category.category_id, tenant_id, uuid4(), "Groceries", None, None)


# ── CreateAccountService ──────────────────────────────────────────────────────

class TestCreateAccountService:
    def test_creates_account_successfully(self):
        tenant_id = uuid4()
        category = _make_category(tenant_id=tenant_id)

        category_repo = MagicMock()
        category_repo.get_by_id.return_value = category

        account_repo = MagicMock()
        account_repo.get_by_name_and_type.return_value = None
        created = _make_account(tenant_id=tenant_id, category_id=category.category_id)
        account_repo.create.return_value = created

        service = CreateAccountService(account_repo, category_repo, _mock_audit())
        result = service.execute(tenant_id, category.category_id, "Salary", None, "INCOME", uuid4())

        assert result.account_id == created.account_id
        account_repo.create.assert_called_once()

    def test_raises_if_category_not_found(self):
        category_repo = MagicMock()
        category_repo.get_by_id.return_value = None

        service = CreateAccountService(MagicMock(), category_repo, _mock_audit())
        with pytest.raises(AccountCategoryNotFoundError):
            service.execute(uuid4(), uuid4(), "Salary", None, "INCOME", uuid4())

    def test_raises_if_account_name_type_exists(self):
        category_repo = MagicMock()
        category_repo.get_by_id.return_value = _make_category()

        account_repo = MagicMock()
        account_repo.get_by_name_and_type.return_value = _make_account()

        service = CreateAccountService(account_repo, category_repo, _mock_audit())
        with pytest.raises(AccountAlreadyExistsError):
            service.execute(uuid4(), uuid4(), "Salary", None, "INCOME", uuid4())


# ── UpdateAccountService ──────────────────────────────────────────────────────

class TestUpdateAccountService:
    def test_deactivates_account(self):
        tenant_id = uuid4()
        account = _make_account(tenant_id=tenant_id, is_active=True)

        account_repo = MagicMock()
        account_repo.get_by_id.return_value = account
        deactivated = _make_account(
            account_id=account.account_id,
            tenant_id=tenant_id,
            is_active=False,
        )
        account_repo.update.return_value = deactivated

        service = UpdateAccountService(account_repo, MagicMock(), _mock_audit())
        result = service.execute(account.account_id, tenant_id, uuid4(), None, None, None, False)

        assert result.is_active is False

    def test_raises_if_account_not_found(self):
        account_repo = MagicMock()
        account_repo.get_by_id.return_value = None

        service = UpdateAccountService(account_repo, MagicMock(), _mock_audit())
        with pytest.raises(AccountNotFoundError):
            service.execute(uuid4(), uuid4(), uuid4(), None, None, None, None)


# ── CreateTransactionService ──────────────────────────────────────────────────

class TestCreateTransactionService:
    def test_creates_transaction_successfully(self):
        tenant_id = uuid4()
        account = _make_account(tenant_id=tenant_id, is_active=True)

        account_repo = MagicMock()
        account_repo.get_by_id.return_value = account

        txn_repo = MagicMock()
        created = _make_transaction(tenant_id=tenant_id, account_id=account.account_id)
        txn_repo.create.return_value = created

        service = CreateTransactionService(txn_repo, account_repo, _mock_audit())
        result = service.execute(
            tenant_id, account.account_id, Decimal("50.00"), "CAD", date.today(), None, "INCOME", uuid4()
        )

        assert result.transaction_id == created.transaction_id
        txn_repo.create.assert_called_once()

    def test_raises_if_account_not_found(self):
        account_repo = MagicMock()
        account_repo.get_by_id.return_value = None

        service = CreateTransactionService(MagicMock(), account_repo, _mock_audit())
        with pytest.raises(AccountNotFoundError):
            service.execute(uuid4(), uuid4(), Decimal("50.00"), "CAD", date.today(), None, "INCOME", uuid4())

    def test_raises_if_account_inactive(self):
        account_repo = MagicMock()
        account_repo.get_by_id.return_value = _make_account(is_active=False)

        service = CreateTransactionService(MagicMock(), account_repo, _mock_audit())
        with pytest.raises(AccountInactiveError):
            service.execute(uuid4(), uuid4(), Decimal("50.00"), "CAD", date.today(), None, "INCOME", uuid4())


# ── UpdateTransactionService ──────────────────────────────────────────────────

class TestUpdateTransactionService:
    def test_updates_amount(self):
        tenant_id = uuid4()
        txn = _make_transaction(tenant_id=tenant_id, amount=Decimal("100.00"))

        txn_repo = MagicMock()
        txn_repo.get_by_id.return_value = txn
        updated = _make_transaction(
            transaction_id=txn.transaction_id,
            tenant_id=tenant_id,
            amount=Decimal("200.00"),
        )
        txn_repo.update.return_value = updated

        service = UpdateTransactionService(txn_repo, MagicMock(), _mock_audit())
        result = service.execute(
            txn.transaction_id, tenant_id, uuid4(),
            None, Decimal("200.00"), None, None, None, None,
        )

        assert result.amount == Decimal("200.00")

    def test_raises_if_transaction_not_found(self):
        txn_repo = MagicMock()
        txn_repo.get_by_id.return_value = None

        service = UpdateTransactionService(txn_repo, MagicMock(), _mock_audit())
        with pytest.raises(TransactionNotFoundError):
            service.execute(uuid4(), uuid4(), uuid4(), None, None, None, None, None, None)


# ── DeleteTransactionService ──────────────────────────────────────────────────

class TestDeleteTransactionService:
    def test_deletes_transaction(self):
        txn = _make_transaction()

        txn_repo = MagicMock()
        txn_repo.get_by_id.return_value = txn

        audit = _mock_audit()
        service = DeleteTransactionService(txn_repo, audit)
        service.execute(txn.transaction_id, txn.tenant_id, uuid4())

        txn_repo.delete.assert_called_once_with(txn.transaction_id, txn.tenant_id)
        audit.log_transaction.assert_called_once()
        audit.log_detail.assert_called_once()

    def test_raises_if_transaction_not_found(self):
        txn_repo = MagicMock()
        txn_repo.get_by_id.return_value = None

        service = DeleteTransactionService(txn_repo, _mock_audit())
        with pytest.raises(TransactionNotFoundError):
            service.execute(uuid4(), uuid4(), uuid4())


# ── BudgetMonthService ───────────────────────────────────────────────────────

class TestBudgetMonthService:
    def test_create_budget_month_success(self):
        repo = MagicMock()
        repo.get_by_month.return_value = None
        repo.create.side_effect = lambda b: b
        audit_repo = MagicMock()
        service = BudgetMonthService(repo, audit_repo)
        tenant_id = uuid4()
        user_id = uuid4()
        month = date(2025, 2, 1)
        result = service.create_budget_month(tenant_id, month, user_id)
        assert result.tenant_id == tenant_id
        assert result.month == month
        assert result.status == "DRAFT"

    def test_create_budget_month_conflict(self):
        repo = MagicMock()
        repo.get_by_month.return_value = _make_budget_month()
        audit_repo = MagicMock()
        service = BudgetMonthService(repo, audit_repo)
        with pytest.raises(Exception):
            service.create_budget_month(uuid4(), date(2025, 2, 1), uuid4())


# ── BudgetAllocationService ───────────────────────────────────────────────────

class TestBudgetAllocationService:
    def test_close_budget_month_success(self):
        repo = MagicMock()
        budget = _make_budget_month()
        repo.get_by_id.return_value = budget
        repo.update.side_effect = lambda b: b
        audit_repo = MagicMock()
        service = BudgetMonthService(repo, audit_repo)
        result = service.close_budget_month(budget.budget_month_id, budget.tenant_id, uuid4())
        assert result.status == "CLOSED"
        assert result.closed_at is not None

    def test_close_budget_month_already_closed(self):
        repo = MagicMock()
        budget = _make_budget_month(status="CLOSED")
        repo.get_by_id.return_value = budget
        audit_repo = MagicMock()
        service = BudgetMonthService(repo, audit_repo)
        with pytest.raises(Exception):
            service.close_budget_month(budget.budget_month_id, budget.tenant_id, uuid4())


    def test_bulk_update_allocations(self):
        repo = MagicMock()
        repo.get_by_budget_and_category.return_value = None
        repo.bulk_update.side_effect = lambda allocs: allocs
        audit_repo = MagicMock()
        service = BudgetAllocationService(repo, audit_repo)
        budget_month_id = uuid4()
        user_id = uuid4()
        allocations = [
            {"category_id": uuid4(), "planned_amount": "100.00"},
            {"category_id": uuid4(), "planned_amount": "200.00"},
        ]
        result = service.bulk_update_allocations(budget_month_id, allocations, user_id)
        assert len(result) == 2
