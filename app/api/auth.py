"""
Authentication middleware for API key validation.

This module provides middleware to validate API keys passed in the X-API-Key header.
"""

from typing import List
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class APIKeyHeader:
    """Custom API key authentication using X-API-Key header."""
    
    def __init__(self, name: str = "X-API-Key"):
        self.name = name
    
    async def __call__(self, request: Request) -> str:
        """Extract and validate API key from request header."""
        api_key = request.headers.get(self.name)
        
        if not api_key:
            logger.warning(f"Missing API key in request to {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required. Please provide X-API-Key header."
            )
        
        # Validate against configured API keys
        valid_api_keys = self._get_valid_api_keys()
        
        if api_key not in valid_api_keys:
            logger.warning(f"Invalid API key attempted for {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key provided."
            )
        
        logger.debug(f"Valid API key authenticated for {request.url.path}")
        return api_key
    
    def _get_valid_api_keys(self) -> List[str]:
        """Get list of valid API keys from configuration."""
        # Handle both single key and comma-separated keys
        if isinstance(settings.api_key, str):
            if "," in settings.api_key:
                return [key.strip() for key in settings.api_key.split(",") if key.strip()]
            else:
                return [settings.api_key]
        return [settings.api_key]


# Global API key dependency
api_key_header = APIKeyHeader()


async def get_api_key(request: Request) -> str:
    """Dependency function to get and validate API key."""
    return await api_key_header(request)


def is_excluded_path(path: str) -> bool:
    """Check if a path should be excluded from authentication."""
    excluded_paths = [
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/health"
    ]
    return path in excluded_paths 