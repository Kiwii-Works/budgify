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


# Authentication Errors

class InvalidCredentialsError(UnauthorizedError):
    """Raised when email or password is incorrect."""
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message, code="INVALID_CREDENTIALS")


class UserInactiveError(BudgifyError):
    """Raised when user is disabled or inactive."""
    def __init__(self, message: str = "User account is inactive"):
        super().__init__(message=message, code="USER_INACTIVE")


class TenantMembershipError(ForbiddenError):
    """Raised when user is not a member of the requested tenant."""
    def __init__(self, message: str = "User is not a member of this tenant"):
        super().__init__(message=message, code="TENANT_MEMBERSHIP_ERROR")


class InvalidTokenError(UnauthorizedError):
    """Raised when JWT token is invalid, malformed, or tampered with."""
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message=message, code="INVALID_TOKEN")


class ExpiredTokenError(UnauthorizedError):
    """Raised when token has expired."""
    def __init__(self, message: str = "Token expired"):
        super().__init__(message=message, code="EXPIRED_TOKEN")


class RevokedTokenError(UnauthorizedError):
    """Raised when refresh token has been revoked."""
    def __init__(self, message: str = "Token has been revoked"):
        super().__init__(message=message, code="REVOKED_TOKEN")
