"""Value objects for identity domain."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Email value object.

    Ensures email format validity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate email format."""
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Validate email format using regex.

        Args:
            email: Email string to validate

        Returns:
            True if valid email format, False otherwise
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        """Return email string."""
        return self.value


@dataclass(frozen=True)
class Password:
    """
    Password value object.

    Represents a hashed password (not plaintext).
    """

    hashed_value: str

    def __post_init__(self) -> None:
        """Validate hashed password is not empty."""
        if not self.hashed_value or not self.hashed_value.strip():
            raise ValueError("Hashed password cannot be empty")

    def __str__(self) -> str:
        """Return masked password for security."""
        return "***REDACTED***"

    def __repr__(self) -> str:
        """Return masked password for security."""
        return "Password(***REDACTED***)"


@dataclass(frozen=True)
class Username:
    """
    Username value object.

    Ensures username validity (alphanumeric, underscores, hyphens, 3-30 chars).
    """

    value: str

    def __post_init__(self) -> None:
        """Validate username format."""
        if not self._is_valid_username(self.value):
            raise ValueError(
                f"Invalid username: {self.value}. "
                "Must be 3-30 characters, alphanumeric with underscores/hyphens."
            )

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        """
        Validate username format.

        Args:
            username: Username to validate

        Returns:
            True if valid username format, False otherwise
        """
        if not 3 <= len(username) <= 30:
            return False
        pattern = r"^[a-zA-Z0-9_-]+$"
        return bool(re.match(pattern, username))

    def __str__(self) -> str:
        """Return username string."""
        return self.value
