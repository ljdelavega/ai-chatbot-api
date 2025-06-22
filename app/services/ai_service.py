"""
Abstract AI service interface for chat functionality.

This module defines the base interface that all AI providers must implement,
enabling easy switching between different AI models and providers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator, Optional
from app.api.models import Message


class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass


class AIProviderError(AIServiceError):
    """Exception raised when AI provider fails."""
    pass


class AIConfigurationError(AIServiceError):
    """Exception raised when AI service is misconfigured."""
    pass


class AIRateLimitError(AIServiceError):
    """Exception raised when AI provider rate limit is exceeded."""
    pass


class BaseAIService(ABC):
    """Abstract base class for AI services."""
    
    @abstractmethod
    async def chat(self, messages: List[Message]) -> str:
        """
        Process a chat conversation and return a complete response.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Complete AI response as string
            
        Raises:
            AIProviderError: When the AI provider fails
            AIConfigurationError: When service is misconfigured
            AIRateLimitError: When rate limit is exceeded
        """
        pass
    
    @abstractmethod
    async def chat_stream(self, messages: List[Message]) -> AsyncGenerator[str, None]:
        """
        Process a chat conversation and return a streaming response.
        
        Args:
            messages: List of conversation messages
            
        Yields:
            Partial AI response chunks as strings
            
        Raises:
            AIProviderError: When the AI provider fails
            AIConfigurationError: When service is misconfigured
            AIRateLimitError: When rate limit is exceeded
        """
        pass
    
    @abstractmethod
    def validate_configuration(self) -> bool:
        """
        Validate that the service is properly configured.
        
        Returns:
            True if configuration is valid
            
        Raises:
            AIConfigurationError: When configuration is invalid
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current AI model.
        
        Returns:
            Dictionary containing model information
        """
        pass 