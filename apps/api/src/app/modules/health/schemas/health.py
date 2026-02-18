"""Health check response schemas."""

from pydantic import BaseModel


class HealthData(BaseModel):
    """Health check data model."""

    status: str


class MetaData(BaseModel):
    """Standard metadata model."""

    request_id: str
    timestamp: str


class HealthResponse(BaseModel):
    """
    Health check response (for documentation/testing only).

    Note: The actual endpoint returns a dict, not this model.
    This model is used for testing assertions and documentation.
    """

    data: HealthData
    meta: MetaData
