"""Domain exceptions for finance module."""

from app.core.errors import BudgifyError, ConflictError, NotFoundError


class AccountCategoryNotFoundError(NotFoundError):
    def __init__(self, message: str = "Account category not found"):
        super().__init__(message=message, code="CATEGORY_NOT_FOUND")


class AccountCategoryAlreadyExistsError(ConflictError):
    def __init__(self, message: str = "Account category already exists"):
        super().__init__(message=message, code="CATEGORY_ALREADY_EXISTS")


class AccountNotFoundError(NotFoundError):
    def __init__(self, message: str = "Account not found"):
        super().__init__(message=message, code="ACCOUNT_NOT_FOUND")


class AccountAlreadyExistsError(ConflictError):
    def __init__(self, message: str = "Account already exists"):
        super().__init__(message=message, code="ACCOUNT_ALREADY_EXISTS")


class AccountInactiveError(BudgifyError):
    def __init__(self, message: str = "Account is inactive"):
        super().__init__(message=message, code="ACCOUNT_INACTIVE")


class TransactionNotFoundError(NotFoundError):
    def __init__(self, message: str = "Transaction not found"):
        super().__init__(message=message, code="TRANSACTION_NOT_FOUND")
