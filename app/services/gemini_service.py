"""
Gemini AI service implementation using LangChain Google GenAI.

This module implements the BaseAIService interface for Google's Gemini models
using the langchain-google-genai integration.
"""

import asyncio
from typing import List, Dict, Any, AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from app.services.ai_service import (
    BaseAIService, 
    AIProviderError, 
    AIConfigurationError, 
    AIRateLimitError
)
from app.api.models import Message
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class GeminiService(BaseAIService):
    """Gemini AI service implementation."""
    
    def __init__(self):
        """Initialize the Gemini service."""
        self.model_name = "gemini-2.0-flash"
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the Gemini client."""
        try:
            if not settings.model_api_key or settings.model_api_key == "test-model-key":
                raise AIConfigurationError(
                    "Gemini API key not configured. Please set MODEL_API_KEY environment variable."
                )
            
            self.client = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=settings.model_api_key,
                temperature=0.7,
                max_tokens=2048,
                max_retries=3,
            )
            
            logger.info(f"Gemini service initialized with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise AIConfigurationError(f"Failed to initialize Gemini client: {str(e)}")
    
    def _convert_messages(self, messages: List[Message]) -> List:
        """
        Convert API messages to LangChain message format.
        
        Args:
            messages: List of API messages
            
        Returns:
            List of LangChain messages
        """
        langchain_messages = []
        
        for message in messages:
            if message.role == "system":
                langchain_messages.append(SystemMessage(content=message.content))
            elif message.role == "user":
                langchain_messages.append(HumanMessage(content=message.content))
            elif message.role == "assistant":
                langchain_messages.append(AIMessage(content=message.content))
            else:
                logger.warning(f"Unknown message role: {message.role}")
                # Default to human message for unknown roles
                langchain_messages.append(HumanMessage(content=message.content))
        
        return langchain_messages
    
    async def chat(self, messages: List[Message]) -> str:
        """
        Process a chat conversation and return a complete response.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Complete AI response as string
        """
        if not self.client:
            raise AIConfigurationError("Gemini client not initialized")
        
        try:
            # Convert messages to LangChain format
            langchain_messages = self._convert_messages(messages)
            
            logger.debug(f"Sending {len(langchain_messages)} messages to Gemini")
            
            # Make async call to Gemini
            response = await self.client.ainvoke(langchain_messages)
            
            logger.debug("Received response from Gemini")
            
            return response.content
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific error types
            if "rate limit" in error_msg or "quota" in error_msg:
                logger.warning(f"Gemini rate limit exceeded: {str(e)}")
                raise AIRateLimitError(f"Gemini rate limit exceeded: {str(e)}")
            elif "api key" in error_msg or "authentication" in error_msg:
                logger.error(f"Gemini authentication error: {str(e)}")
                raise AIConfigurationError(f"Gemini authentication error: {str(e)}")
            elif "permission" in error_msg or "forbidden" in error_msg:
                logger.error(f"Gemini permission error: {str(e)}")
                raise AIConfigurationError(f"Gemini permission error: {str(e)}")
            else:
                logger.error(f"Gemini provider error: {str(e)}")
                raise AIProviderError(f"Gemini provider error: {str(e)}")
    
    async def chat_stream(self, messages: List[Message]) -> AsyncGenerator[str, None]:
        """
        Process a chat conversation and return a streaming response.
        
        Args:
            messages: List of conversation messages
            
        Yields:
            Partial AI response chunks as strings
        """
        if not self.client:
            raise AIConfigurationError("Gemini client not initialized")
        
        try:
            # Convert messages to LangChain format
            langchain_messages = self._convert_messages(messages)
            
            logger.debug(f"Starting streaming response from Gemini for {len(langchain_messages)} messages")
            
            # Stream response from Gemini
            async for chunk in self.client.astream(langchain_messages):
                if chunk.content:
                    yield chunk.content
            
            logger.debug("Completed streaming response from Gemini")
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific error types
            if "rate limit" in error_msg or "quota" in error_msg:
                logger.warning(f"Gemini rate limit exceeded during streaming: {str(e)}")
                raise AIRateLimitError(f"Gemini rate limit exceeded: {str(e)}")
            elif "api key" in error_msg or "authentication" in error_msg:
                logger.error(f"Gemini authentication error during streaming: {str(e)}")
                raise AIConfigurationError(f"Gemini authentication error: {str(e)}")
            elif "permission" in error_msg or "forbidden" in error_msg:
                logger.error(f"Gemini permission error during streaming: {str(e)}")
                raise AIConfigurationError(f"Gemini permission error: {str(e)}")
            else:
                logger.error(f"Gemini provider error during streaming: {str(e)}")
                raise AIProviderError(f"Gemini provider error: {str(e)}")
    
    def validate_configuration(self) -> bool:
        """
        Validate that the service is properly configured.
        
        Returns:
            True if configuration is valid
        """
        try:
            if not settings.model_api_key or settings.model_api_key == "test-model-key":
                raise AIConfigurationError("Gemini API key not configured")
            
            if not self.client:
                raise AIConfigurationError("Gemini client not initialized")
            
            logger.debug("Gemini service configuration is valid")
            return True
            
        except Exception as e:
            logger.error(f"Gemini configuration validation failed: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current AI model.
        
        Returns:
            Dictionary containing model information
        """
        return {
            "provider": "google",
            "model": self.model_name,
            "type": "chat",
            "capabilities": ["text", "streaming"],
            "max_tokens": 2048,
            "configured": self.client is not None
        } 