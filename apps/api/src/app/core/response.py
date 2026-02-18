"""Standard response wrappers for API endpoints."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def create_success_response(data: Any, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Create a standard success response.

    Args:
        data: Response data payload
        meta: Optional additional metadata

    Returns:
        Standardized success response dict

    Example:
        >>> create_success_response({"status": "ok"})
        {
            "data": {"status": "ok"},
            "meta": {
                "request_id": "...",
                "timestamp": "2024-01-01T12:00:00.000000"
            }
        }
    """
    base_meta = {
        "request_id": str(uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
    }

    if meta:
        base_meta.update(meta)

    return {"data": data, "meta": base_meta}


def create_error_response(
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a standard error response.

    Args:
        code: Error code
        message: Human-readable error message
        details: Optional list of detailed error information
        meta: Optional additional metadata

    Returns:
        Standardized error response dict

    Example:
        >>> create_error_response("ValidationError", "Invalid input", [{"field": "email"}])
        {
            "error": {
                "code": "ValidationError",
                "message": "Invalid input",
                "details": [{"field": "email"}]
            },
            "meta": {
                "request_id": "...",
                "timestamp": "2024-01-01T12:00:00.000000"
            }
        }
    """
    base_meta = {
        "request_id": str(uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
    }

    if meta:
        base_meta.update(meta)

    error_payload = {
        "code": code,
        "message": message,
        "details": details or [],
    }

    return {"error": error_payload, "meta": base_meta}


def create_paginated_response(
    data: list[Any],
    page: int,
    page_size: int,
    total: int,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a paginated response.

    Args:
        data: List of response items
        page: Current page number
        page_size: Number of items per page
        total: Total number of items
        meta: Optional additional metadata

    Returns:
        Standardized paginated response dict

    Example:
        >>> create_paginated_response([{"id": 1}], page=1, page_size=20, total=100)
        {
            "data": [{"id": 1}],
            "meta": {
                "request_id": "...",
                "timestamp": "...",
                "pagination": {
                    "page": 1,
                    "page_size": 20,
                    "total": 100
                }
            }
        }
    """
    base_meta = {
        "request_id": str(uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    }

    if meta:
        base_meta.update(meta)

    return {"data": data, "meta": base_meta}
