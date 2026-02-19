"""Concrete repository implementations for finance module."""

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.finance.domain.entities import Account, AccountCategory, Transaction
from app.modules.finance.infrastructure.models import (
    Account as AccountModel,
    AccountCategory as AccountCategoryModel,
    FinancialTransaction as TransactionModel,
)
from app.modules.identity.infrastructure.models import OperationType


class SQLAlchemyAccountCategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, category: AccountCategory) -> AccountCategory:
        model = AccountCategoryModel(
            category_id=category.category_id,
            tenant_id=category.tenant_id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_by=category.created_by,
            modified_by=category.modified_by,
            created_date=category.created_date,
            created_date_utc=category.created_date_utc,
            modified_date=category.modified_date,
            modified_date_utc=category.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(category, "transaction_uid", None),
        )
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)

    def get_by_id(self, category_id: UUID, tenant_id: UUID) -> AccountCategory | None:
        model = (
            self.session.query(AccountCategoryModel)
            .filter(
                AccountCategoryModel.category_id == category_id,
                AccountCategoryModel.tenant_id == tenant_id,
            )
            .first()
        )
        return self._to_entity(model) if model else None

    def get_by_name(self, name: str, tenant_id: UUID) -> AccountCategory | None:
        model = (
            self.session.query(AccountCategoryModel)
            .filter(
                func.lower(AccountCategoryModel.name) == name.lower(),
                AccountCategoryModel.tenant_id == tenant_id,
            )
            .first()
        )
        return self._to_entity(model) if model else None

    def list(self, tenant_id: UUID, page: int, page_size: int) -> tuple[list[AccountCategory], int]:
        query = self.session.query(AccountCategoryModel).filter(
            AccountCategoryModel.tenant_id == tenant_id
        )
        total = query.count()
        models = query.offset((page - 1) * page_size).limit(page_size).all()
        return [self._to_entity(m) for m in models], total

    def update(self, category: AccountCategory) -> AccountCategory:
        model = (
            self.session.query(AccountCategoryModel)
            .filter(AccountCategoryModel.category_id == category.category_id)
            .first()
        )
        if model:
            model.name = category.name
            model.description = category.description
            model.is_active = category.is_active
            model.modified_by = category.modified_by
            model.modified_date = category.modified_date
            model.modified_date_utc = category.modified_date_utc
            model.operation_type = OperationType.MODIFIED
            model.transaction_uid = getattr(category, "transaction_uid", None)
            self.session.flush()
        return self._to_entity(model)

    def _to_entity(self, model: AccountCategoryModel) -> AccountCategory:
        return AccountCategory(
            category_id=model.category_id,
            tenant_id=model.tenant_id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyAccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, account: Account) -> Account:
        model = AccountModel(
            account_id=account.account_id,
            tenant_id=account.tenant_id,
            category_id=account.category_id,
            name=account.name,
            description=account.description,
            type=account.type,
            is_active=account.is_active,
            created_by=account.created_by,
            modified_by=account.modified_by,
            created_date=account.created_date,
            created_date_utc=account.created_date_utc,
            modified_date=account.modified_date,
            modified_date_utc=account.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(account, "transaction_uid", None),
        )
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)

    def get_by_id(self, account_id: UUID, tenant_id: UUID) -> Account | None:
        model = (
            self.session.query(AccountModel)
            .filter(
                AccountModel.account_id == account_id,
                AccountModel.tenant_id == tenant_id,
            )
            .first()
        )
        return self._to_entity(model) if model else None

    def get_by_name_and_type(self, name: str, type: str, tenant_id: UUID) -> Account | None:
        model = (
            self.session.query(AccountModel)
            .filter(
                func.lower(AccountModel.name) == name.lower(),
                AccountModel.type == type,
                AccountModel.tenant_id == tenant_id,
            )
            .first()
        )
        return self._to_entity(model) if model else None

    def list(self, tenant_id: UUID, page: int, page_size: int) -> tuple[list[Account], int]:
        query = self.session.query(AccountModel).filter(AccountModel.tenant_id == tenant_id)
        total = query.count()
        models = query.offset((page - 1) * page_size).limit(page_size).all()
        return [self._to_entity(m) for m in models], total

    def update(self, account: Account) -> Account:
        model = (
            self.session.query(AccountModel)
            .filter(AccountModel.account_id == account.account_id)
            .first()
        )
        if model:
            model.name = account.name
            model.description = account.description
            model.is_active = account.is_active
            model.category_id = account.category_id
            model.modified_by = account.modified_by
            model.modified_date = account.modified_date
            model.modified_date_utc = account.modified_date_utc
            model.operation_type = OperationType.MODIFIED
            model.transaction_uid = getattr(account, "transaction_uid", None)
            self.session.flush()
        return self._to_entity(model)

    def _to_entity(self, model: AccountModel) -> Account:
        return Account(
            account_id=model.account_id,
            tenant_id=model.tenant_id,
            category_id=model.category_id,
            name=model.name,
            description=model.description,
            type=model.type,
            is_active=model.is_active,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )


class SQLAlchemyTransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        model = TransactionModel(
            transaction_id=transaction.transaction_id,
            tenant_id=transaction.tenant_id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            currency=transaction.currency,
            occurred_on=transaction.occurred_on,
            notes=transaction.notes,
            direction=transaction.direction,
            created_by=transaction.created_by,
            modified_by=transaction.modified_by,
            created_date=transaction.created_date,
            created_date_utc=transaction.created_date_utc,
            modified_date=transaction.modified_date,
            modified_date_utc=transaction.modified_date_utc,
            operation_type=OperationType.ADDED,
            transaction_uid=getattr(transaction, "transaction_uid", None),
        )
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)

    def get_by_id(self, transaction_id: UUID, tenant_id: UUID) -> Transaction | None:
        model = (
            self.session.query(TransactionModel)
            .filter(
                TransactionModel.transaction_id == transaction_id,
                TransactionModel.tenant_id == tenant_id,
            )
            .first()
        )
        return self._to_entity(model) if model else None

    def list(
        self,
        tenant_id: UUID,
        page: int,
        page_size: int,
        account_id: UUID | None = None,
        direction: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> tuple[list[Transaction], int]:
        query = self.session.query(TransactionModel).filter(TransactionModel.tenant_id == tenant_id)
        if account_id:
            query = query.filter(TransactionModel.account_id == account_id)
        if direction:
            query = query.filter(TransactionModel.direction == direction)
        if from_date:
            query = query.filter(TransactionModel.occurred_on >= from_date)
        if to_date:
            query = query.filter(TransactionModel.occurred_on <= to_date)
        total = query.count()
        models = query.order_by(TransactionModel.occurred_on.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return [self._to_entity(m) for m in models], total

    def update(self, transaction: Transaction) -> Transaction:
        model = (
            self.session.query(TransactionModel)
            .filter(TransactionModel.transaction_id == transaction.transaction_id)
            .first()
        )
        if model:
            model.account_id = transaction.account_id
            model.amount = transaction.amount
            model.currency = transaction.currency
            model.occurred_on = transaction.occurred_on
            model.notes = transaction.notes
            model.direction = transaction.direction
            model.modified_by = transaction.modified_by
            model.modified_date = transaction.modified_date
            model.modified_date_utc = transaction.modified_date_utc
            model.operation_type = OperationType.MODIFIED
            model.transaction_uid = getattr(transaction, "transaction_uid", None)
            self.session.flush()
        return self._to_entity(model)

    def delete(self, transaction_id: UUID, tenant_id: UUID) -> None:
        self.session.query(TransactionModel).filter(
            TransactionModel.transaction_id == transaction_id,
            TransactionModel.tenant_id == tenant_id,
        ).delete()
        self.session.flush()

    def _to_entity(self, model: TransactionModel) -> Transaction:
        return Transaction(
            transaction_id=model.transaction_id,
            tenant_id=model.tenant_id,
            account_id=model.account_id,
            amount=Decimal(str(model.amount)),
            currency=model.currency,
            occurred_on=model.occurred_on,
            notes=model.notes,
            direction=model.direction,
            created_by=model.created_by,
            modified_by=model.modified_by,
            created_date=model.created_date,
            created_date_utc=model.created_date_utc,
            modified_date=model.modified_date,
            modified_date_utc=model.modified_date_utc,
        )
