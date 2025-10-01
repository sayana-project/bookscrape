"""
Logging configuration for the application.
"""
import logging
import sys
from typing import Dict, Any


def setup_logging(level: str = "INFO") -> None:
    """
    Setup logging configuration for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Configure specific loggers
    loggers_config = {
        "book_api": level.upper(),
        "sqlalchemy.engine": "WARNING",  # Reduce SQLAlchemy noise
        "uvicorn": "INFO"
    }

    for logger_name, logger_level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, logger_level))


def get_typed_logger(name: str) -> logging.Logger:
    """
    Get a typed logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)