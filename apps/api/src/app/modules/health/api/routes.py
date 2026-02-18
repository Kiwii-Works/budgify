"""Health check endpoint routes."""

from typing import Any

from fastapi import APIRouter

from app.core.response import create_success_response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check() -> dict[str, Any]:
    """
    Basic health check endpoint.

    Returns standard response shape per API_CONTRACT.md.
    No response_model - contract is validated in tests.

    Returns:
        Standard success response with status: ok
    """
    return create_success_response({"status": "ok"})
