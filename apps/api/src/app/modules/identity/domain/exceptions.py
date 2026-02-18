"""Domain exceptions for identity module."""


class IdentityDomainError(Exception):
    """Base exception for identity domain errors."""

    pass


class UserAlreadyExistsError(IdentityDomainError):
    """User with username/email/phone already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"User with {field}='{value}' already exists")


class TenantNotFoundError(IdentityDomainError):
    """Tenant does not exist."""

    pass


class UserNotFoundError(IdentityDomainError):
    """User does not exist."""

    pass


class RoleNotFoundError(IdentityDomainError):
    """Role does not exist."""

    pass


class InvalidPasswordError(IdentityDomainError):
    """Password does not meet requirements."""

    pass


class ForbiddenError(IdentityDomainError):
    """User lacks permission."""

    pass
