"""Custom exception classes for the application."""

from typing import Any


class BudgifyError(Exception):
    """Base exception for all Budgify application errors."""

    def __init__(self, message: str, code: str | None = None, details: Any = None) -> None:
        """
        Initialize error.

        Args:
            message: Human-readable error message
            code: Error code for client identification
            details: Additional error details (e.g., validation errors)
        """
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or []
        super().__init__(self.message)


class ValidationError(BudgifyError):
    """Raised when input validation fails."""

    pass


class NotFoundError(BudgifyError):
    """Raised when a resource is not found."""

    pass


class UnauthorizedError(BudgifyError):
    """Raised when authentication fails or is missing."""

    pass


class ForbiddenError(BudgifyError):
    """Raised when user lacks permission for an action."""

    pass


class ConflictError(BudgifyError):
    """Raised when a resource conflict occurs (e.g., duplicate)."""

    pass


class DatabaseError(BudgifyError):
    """Raised when a database operation fails."""

    pass
