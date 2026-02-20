"""Finance API routes."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies.auth import CurrentUser, get_current_user
from app.core.errors import ConflictError, NotFoundError
from app.core.response import create_paginated_response, create_success_response
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
from app.modules.finance.domain.exceptions import AccountInactiveError
from app.modules.finance.infrastructure.repositories import (
    SQLAlchemyAccountCategoryRepository,
    SQLAlchemyAccountRepository,
    SQLAlchemyTransactionRepository,
    SQLAlchemyBudgetMonthRepository,
    SQLAlchemyBudgetAllocationRepository,
    SQLAlchemyWalletAccountRepository,
)
from app.modules.finance.schemas.finance import (
    AccountResponse,
    CategoryResponse,
    CreateAccountRequest,
    CreateCategoryRequest,
    CreateTransactionRequest,
    TransactionResponse,
    UpdateAccountRequest,
    UpdateCategoryRequest,
    UpdateTransactionRequest,
    BudgetMonthCreateRequest,
    BudgetMonthResponse,
    BudgetAllocationRequest,
    BudgetAllocationResponse,
    BudgetSummaryResponse,
    CreateWalletAccountRequest,
    UpdateWalletAccountRequest,
    WalletAccountResponse,
)

router = APIRouter(tags=["finance"])

# ── Wallet Accounts ─────────────────────────────────────────────────────────

@router.post("/wallet-accounts", status_code=status.HTTP_201_CREATED)
async def create_wallet_account(
    request: CreateWalletAccountRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    repo = SQLAlchemyWalletAccountRepository(db)
    service = WalletAccountService(repo)
    from uuid import uuid4
    from decimal import Decimal
    entity = service.create_wallet_account(
        wallet_account=request_to_entity(request, current_user.tenant_id, uuid4())
    )
    return create_success_response(WalletAccountResponse(
        wallet_account_id=str(entity.wallet_account_id),
        tenant_id=str(entity.tenant_id),
        name=entity.name,
        type=entity.type,
        currency=entity.currency,
        opening_balance=entity.opening_balance,
        is_active=entity.is_active,
    ).model_dump())


@router.get("/wallet-accounts")
async def list_wallet_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = SQLAlchemyWalletAccountRepository(db)
    service = WalletAccountService(repo)
    items, total = service.list_wallet_accounts(current_user.tenant_id, page, page_size)
    return create_paginated_response(
        data=[WalletAccountResponse(
            wallet_account_id=str(a.wallet_account_id),
            tenant_id=str(a.tenant_id),
            name=a.name,
            type=a.type,
            currency=a.currency,
            opening_balance=a.opening_balance,
            is_active=a.is_active,
        ).model_dump() for a in items],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.patch("/wallet-accounts/{wallet_account_id}")
async def update_wallet_account(
    wallet_account_id: UUID,
    request: UpdateWalletAccountRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    repo = SQLAlchemyWalletAccountRepository(db)
    service = WalletAccountService(repo)
    entity = service.get_wallet_account(wallet_account_id, current_user.tenant_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Wallet account not found")
    # Update fields
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(entity, field, value)
    updated = service.update_wallet_account(entity)
    return create_success_response(WalletAccountResponse(
        wallet_account_id=str(updated.wallet_account_id),
        tenant_id=str(updated.tenant_id),
        name=updated.name,
        type=updated.type,
        currency=updated.currency,
        opening_balance=updated.opening_balance,
        is_active=updated.is_active,
    ).model_dump())


@router.delete("/wallet-accounts/{wallet_account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_wallet_account(
    wallet_account_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_sudo(current_user)
    repo = SQLAlchemyWalletAccountRepository(db)
    service = WalletAccountService(repo)
    entity = service.get_wallet_account(wallet_account_id, current_user.tenant_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Wallet account not found")
    service.deactivate_wallet_account(wallet_account_id, current_user.tenant_id)
    return None


# --- Helper ---
def request_to_entity(request: CreateWalletAccountRequest, tenant_id: UUID, wallet_account_id: UUID):
    from decimal import Decimal
    return WalletAccount(
        wallet_account_id=wallet_account_id,
        tenant_id=tenant_id,
        name=request.name,
        type=request.type.value if hasattr(request.type, 'value') else str(request.type),
        currency=request.currency,
        opening_balance=Decimal(request.opening_balance),
        is_active=True,
    )
from app.modules.identity.infrastructure.repositories import SQLAlchemyAuditRepository

router = APIRouter(prefix="/finance", tags=["finance"])

_EDITOR_ROLES = ["SUDO", "EDITOR"]


def _require_editor(current_user: CurrentUser) -> None:
    if not current_user.has_any_role(_EDITOR_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions: SUDO or EDITOR role required",
        )


def _require_sudo(current_user: CurrentUser) -> None:
    if not current_user.has_role("SUDO"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions: SUDO role required",
        )


# ── Account Categories ────────────────────────────────────────────────────────

@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    request: CreateCategoryRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    try:
        category_repo = SQLAlchemyAccountCategoryRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = CreateCategoryService(category_repo, audit_repo)
        created = service.execute(
            tenant_id=current_user.tenant_id,
            name=request.name,
            description=request.description,
            user_id=current_user.user_id,
        )
        db.commit()
        return create_success_response(
            CategoryResponse(
                category_id=str(created.category_id),
                tenant_id=str(created.tenant_id),
                name=created.name,
                description=created.description,
                is_active=created.is_active,
            ).model_dump()
        )
    except ConflictError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/categories")
async def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category_repo = SQLAlchemyAccountCategoryRepository(db)
    items, total = category_repo.list(current_user.tenant_id, page, page_size)
    return create_paginated_response(
        data=[
            CategoryResponse(
                category_id=str(c.category_id),
                tenant_id=str(c.tenant_id),
                name=c.name,
                description=c.description,
                is_active=c.is_active,
            ).model_dump()
            for c in items
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.patch("/categories/{category_id}")
async def update_category(
    category_id: UUID,
    request: UpdateCategoryRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    try:
        category_repo = SQLAlchemyAccountCategoryRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = UpdateCategoryService(category_repo, audit_repo)
        updated = service.execute(
            category_id=category_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            name=request.name,
            description=request.description,
            is_active=request.is_active,
        )
        db.commit()
        return create_success_response(
            CategoryResponse(
                category_id=str(updated.category_id),
                tenant_id=str(updated.tenant_id),
                name=updated.name,
                description=updated.description,
                is_active=updated.is_active,
            ).model_dump()
        )
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except ConflictError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_category(
    category_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_sudo(current_user)
    try:
        category_repo = SQLAlchemyAccountCategoryRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = UpdateCategoryService(category_repo, audit_repo)
        service.execute(
            category_id=category_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            name=None,
            description=None,
            is_active=False,
        )
        db.commit()
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# ── Accounts ──────────────────────────────────────────────────────────────────

@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    request: CreateAccountRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    try:
        account_repo = SQLAlchemyAccountRepository(db)
        category_repo = SQLAlchemyAccountCategoryRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = CreateAccountService(account_repo, category_repo, audit_repo)
        created = service.execute(
            tenant_id=current_user.tenant_id,
            category_id=request.category_id,
            name=request.name,
            description=request.description,
            type=request.type,
            user_id=current_user.user_id,
        )
        db.commit()
        return create_success_response(
            AccountResponse(
                account_id=str(created.account_id),
                tenant_id=str(created.tenant_id),
                category_id=str(created.category_id),
                name=created.name,
                description=created.description,
                type=created.type,
                is_active=created.is_active,
            ).model_dump()
        )
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except ConflictError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/accounts")
async def list_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account_repo = SQLAlchemyAccountRepository(db)
    items, total = account_repo.list(current_user.tenant_id, page, page_size)
    return create_paginated_response(
        data=[
            AccountResponse(
                account_id=str(a.account_id),
                tenant_id=str(a.tenant_id),
                category_id=str(a.category_id),
                name=a.name,
                description=a.description,
                type=a.type,
                is_active=a.is_active,
            ).model_dump()
            for a in items
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.patch("/accounts/{account_id}")
async def update_account(
    account_id: UUID,
    request: UpdateAccountRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    try:
        account_repo = SQLAlchemyAccountRepository(db)
        category_repo = SQLAlchemyAccountCategoryRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = UpdateAccountService(account_repo, category_repo, audit_repo)
        updated = service.execute(
            account_id=account_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            category_id=request.category_id,
            name=request.name,
            description=request.description,
            is_active=request.is_active,
        )
        db.commit()
        return create_success_response(
            AccountResponse(
                account_id=str(updated.account_id),
                tenant_id=str(updated.tenant_id),
                category_id=str(updated.category_id),
                name=updated.name,
                description=updated.description,
                type=updated.type,
                is_active=updated.is_active,
            ).model_dump()
        )
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except ConflictError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_account(
    account_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_sudo(current_user)
    try:
        account_repo = SQLAlchemyAccountRepository(db)
        category_repo = SQLAlchemyAccountCategoryRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = UpdateAccountService(account_repo, category_repo, audit_repo)
        service.execute(
            account_id=account_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            category_id=None,
            name=None,
            description=None,
            is_active=False,
        )
        db.commit()
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# ── Transactions ──────────────────────────────────────────────────────────────

@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    request: CreateTransactionRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    try:
        transaction_repo = SQLAlchemyTransactionRepository(db)
        account_repo = SQLAlchemyAccountRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = CreateTransactionService(transaction_repo, account_repo, audit_repo)
        created = service.execute(
            tenant_id=current_user.tenant_id,
            account_id=request.account_id,
            amount=request.amount,
            currency=request.currency,
            occurred_on=request.occurred_on,
            notes=request.notes,
            direction=request.direction,
            user_id=current_user.user_id,
        )
        db.commit()
        return create_success_response(
            TransactionResponse(
                transaction_id=str(created.transaction_id),
                tenant_id=str(created.tenant_id),
                account_id=str(created.account_id),
                amount=str(created.amount),
                currency=created.currency,
                occurred_on=created.occurred_on.isoformat(),
                notes=created.notes,
                direction=created.direction,
            ).model_dump()
        )
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except AccountInactiveError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/transactions")
async def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    account_id: UUID | None = Query(None),
    direction: str | None = Query(None, pattern="^(INCOME|EXPENSE)$"),
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transaction_repo = SQLAlchemyTransactionRepository(db)
    items, total = transaction_repo.list(
        tenant_id=current_user.tenant_id,
        page=page,
        page_size=page_size,
        account_id=account_id,
        direction=direction,
        from_date=from_date,
        to_date=to_date,
    )
    return create_paginated_response(
        data=[
            TransactionResponse(
                transaction_id=str(t.transaction_id),
                tenant_id=str(t.tenant_id),
                account_id=str(t.account_id),
                amount=str(t.amount),
                currency=t.currency,
                occurred_on=t.occurred_on.isoformat(),
                notes=t.notes,
                direction=t.direction,
            ).model_dump()
            for t in items
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/transactions/{transaction_id}")
async def get_transaction(
    transaction_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transaction_repo = SQLAlchemyTransactionRepository(db)
    txn = transaction_repo.get_by_id(transaction_id, current_user.tenant_id)
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return create_success_response(
        TransactionResponse(
            transaction_id=str(txn.transaction_id),
            tenant_id=str(txn.tenant_id),
            account_id=str(txn.account_id),
            amount=str(txn.amount),
            currency=txn.currency,
            occurred_on=txn.occurred_on.isoformat(),
            notes=txn.notes,
            direction=txn.direction,
        ).model_dump()
    )


@router.patch("/transactions/{transaction_id}")
async def update_transaction(
    transaction_id: UUID,
    request: UpdateTransactionRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_editor(current_user)
    try:
        transaction_repo = SQLAlchemyTransactionRepository(db)
        account_repo = SQLAlchemyAccountRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = UpdateTransactionService(transaction_repo, account_repo, audit_repo)
        updated = service.execute(
            transaction_id=transaction_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            account_id=request.account_id,
            amount=request.amount,
            currency=request.currency,
            occurred_on=request.occurred_on,
            notes=request.notes,
            direction=request.direction,
        )
        db.commit()
        return create_success_response(
            TransactionResponse(
                transaction_id=str(updated.transaction_id),
                tenant_id=str(updated.tenant_id),
                account_id=str(updated.account_id),
                amount=str(updated.amount),
                currency=updated.currency,
                occurred_on=updated.occurred_on.isoformat(),
                notes=updated.notes,
                direction=updated.direction,
            ).model_dump()
        )
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except AccountInactiveError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_sudo(current_user)
    try:
        transaction_repo = SQLAlchemyTransactionRepository(db)
        audit_repo = SQLAlchemyAuditRepository(db)
        service = DeleteTransactionService(transaction_repo, audit_repo)
        service.execute(
            transaction_id=transaction_id,
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
        )
        db.commit()
    except NotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# ── Budgets ──────────────────────────────────────────────────────────────────

@router.post("/budgets", response_model=BudgetMonthResponse, status_code=status.HTTP_201_CREATED)
async def create_budget_month(
    req: BudgetMonthCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _require_editor(current_user)
    repo = SQLAlchemyBudgetMonthRepository(db)
    audit_repo = SQLAlchemyAuditRepository(db)
    service = BudgetMonthService(repo, audit_repo)
    try:
        budget = service.create_budget_month(current_user.tenant_id, req.month, current_user.user_id, req.currency)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
    return create_success_response(BudgetMonthResponse(**budget.__dict__))


@router.get("/budgets/by-month", response_model=BudgetMonthResponse)
async def get_budget_month_by_month(
    month: date = Query(...),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    repo = SQLAlchemyBudgetMonthRepository(db)
    audit_repo = SQLAlchemyAuditRepository(db)
    service = BudgetMonthService(repo, audit_repo)
    budget = service.get_budget_month(current_user.tenant_id, month)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget month not found")
    return create_success_response(BudgetMonthResponse(**budget.__dict__))


@router.put("/budgets/{budget_month_id}/allocations", response_model=list[BudgetAllocationResponse])
async def bulk_update_allocations(
    budget_month_id: UUID,
    req: list[BudgetAllocationRequest],
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _require_editor(current_user)
    repo = SQLAlchemyBudgetAllocationRepository(db)
    audit_repo = SQLAlchemyAuditRepository(db)
    service = BudgetAllocationService(repo, audit_repo)
    allocations = service.bulk_update_allocations(budget_month_id, [a.dict() for a in req], current_user.user_id)
    return [BudgetAllocationResponse(**a.__dict__) for a in allocations]


@router.post("/budgets/{budget_month_id}/close", response_model=BudgetMonthResponse)
async def close_budget_month(
    budget_month_id: UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _require_sudo(current_user)
    repo = SQLAlchemyBudgetMonthRepository(db)
    audit_repo = SQLAlchemyAuditRepository(db)
    service = BudgetMonthService(repo, audit_repo)
    try:
        budget = service.close_budget_month(budget_month_id, current_user.tenant_id, current_user.user_id)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
    return create_success_response(BudgetMonthResponse(**budget.__dict__))
