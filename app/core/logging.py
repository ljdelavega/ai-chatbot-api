"""
Logging configuration for the AI Chatbot API.

This module sets up structured logging with configurable levels
and JSON output for production readiness.
"""

import logging
import logging.config
import sys
from typing import Dict, Any

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    
    Sets up logging with:
    - Configurable log level from environment
    - JSON formatting for production
    - Console output with proper formatting
    - Request ID correlation (for future use)
    """
    
    # Define log level mapping
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    # Get log level from settings, default to INFO
    log_level = log_levels.get(settings.log_level.upper(), logging.INFO)
    
    # Configure logging
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - "
                    "%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": (
                    "%(asctime)s %(name)s %(levelname)s %(filename)s "
                    "%(lineno)d %(funcName)s %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed" if log_level == logging.DEBUG else "default",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "app": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn": {
                "level": logging.INFO,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": logging.INFO,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": logging.INFO,
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {
            "level": log_level,
            "handlers": ["console"],
        },
    }
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)
    
    # Log startup message
    logger = logging.getLogger("app.core.logging")
    logger.info(
        f"Logging configured - Level: {settings.log_level.upper()}, "
        f"Provider: {settings.model_provider}"
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"app.{name}")


# Convenience function for getting module loggers
def get_module_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        module_name: Name of the module (e.g., 'api.chat')
        
    Returns:
        Logger instance for the module
    """
    return get_logger(module_name) 