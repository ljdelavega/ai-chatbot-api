"""
AI service factory for creating and managing AI service instances.

This module provides a factory pattern for creating AI services based on
configuration, enabling easy switching between different AI providers.
"""

from typing import Dict, Type
from app.services.ai_service import BaseAIService, AIConfigurationError
from app.services.gemini_service import GeminiService
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIServiceFactory:
    """Factory for creating AI service instances."""
    
    # Registry of available AI services
    _services: Dict[str, Type[BaseAIService]] = {
        "gemini": GeminiService,
    }
    
    # Singleton instance cache
    _instance_cache: Dict[str, BaseAIService] = {}
    
    @classmethod
    def create_service(cls, provider: str = None) -> BaseAIService:
        """
        Create or retrieve an AI service instance.
        
        Args:
            provider: AI provider name (defaults to settings.model_provider)
            
        Returns:
            AI service instance
            
        Raises:
            AIConfigurationError: When provider is not supported or configured
        """
        if provider is None:
            provider = settings.model_provider.lower()
        
        provider = provider.lower()
        
        # Check if we already have a cached instance
        if provider in cls._instance_cache:
            logger.debug(f"Returning cached {provider} service instance")
            return cls._instance_cache[provider]
        
        # Check if provider is supported
        if provider not in cls._services:
            available_providers = list(cls._services.keys())
            raise AIConfigurationError(
                f"Unsupported AI provider: {provider}. "
                f"Available providers: {available_providers}"
            )
        
        try:
            # Create new service instance
            service_class = cls._services[provider]
            service_instance = service_class()
            
            # Validate configuration
            service_instance.validate_configuration()
            
            # Cache the instance
            cls._instance_cache[provider] = service_instance
            
            logger.info(f"Created and cached {provider} service instance")
            return service_instance
            
        except Exception as e:
            logger.error(f"Failed to create {provider} service: {str(e)}")
            raise AIConfigurationError(f"Failed to create {provider} service: {str(e)}")
    
    @classmethod
    def get_default_service(cls) -> BaseAIService:
        """
        Get the default AI service based on configuration.
        
        Returns:
            Default AI service instance
        """
        return cls.create_service()
    
    @classmethod
    def register_service(cls, name: str, service_class: Type[BaseAIService]) -> None:
        """
        Register a new AI service provider.
        
        Args:
            name: Provider name
            service_class: Service class implementing BaseAIService
        """
        cls._services[name.lower()] = service_class
        logger.info(f"Registered AI service provider: {name}")
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """
        List all available AI providers.
        
        Returns:
            List of provider names
        """
        return list(cls._services.keys())
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear the service instance cache."""
        cls._instance_cache.clear()
        logger.debug("Cleared AI service instance cache")


# Convenience function for getting the default service
def get_ai_service() -> BaseAIService:
    """
    Get the default AI service instance.
    
    Returns:
        AI service instance
    """
    return AIServiceFactory.get_default_service() 