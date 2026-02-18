"""Centralized logging configuration."""

import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """Configure application-wide logging."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Root logger configuration
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Set uvicorn loggers to same level
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(log_level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Module logger
logger = get_logger(__name__)
