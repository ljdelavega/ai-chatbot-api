"""
Tests for AI service implementations.

This module contains unit tests for the AI service layer, including
mocked responses and error scenarios.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import List

from app.services.ai_service import (
    BaseAIService, 
    AIServiceError, 
    AIProviderError, 
    AIConfigurationError, 
    AIRateLimitError
)
from app.services.gemini_service import GeminiService
from app.services.ai_factory import AIServiceFactory, get_ai_service
from app.api.models import Message


class TestGeminiService:
    """Test cases for GeminiService."""
    
    @pytest.fixture
    def mock_settings(self):
        """Mock settings with valid API key."""
        with patch('app.services.gemini_service.settings') as mock:
            mock.model_api_key = "test-valid-api-key"
            mock.model_provider = "gemini"
            yield mock
    
    @pytest.fixture
    def mock_chat_client(self):
        """Mock ChatGoogleGenerativeAI client."""
        with patch('app.services.gemini_service.ChatGoogleGenerativeAI') as mock:
            yield mock
    
    @pytest.fixture
    def sample_messages(self):
        """Sample conversation messages."""
        return [
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello, how are you?"),
            Message(role="assistant", content="I'm doing well, thank you!"),
            Message(role="user", content="What's the weather like?")
        ]
    
    def test_initialization_success(self, mock_settings, mock_chat_client):
        """Test successful service initialization."""
        service = GeminiService()
        
        assert service.model_name == "gemini-2.0-flash"
        assert service.client is not None
        mock_chat_client.assert_called_once()
    
    def test_initialization_missing_api_key(self, mock_chat_client):
        """Test initialization failure with missing API key."""
        with patch('app.services.gemini_service.settings') as mock_settings:
            mock_settings.model_api_key = "test-model-key"  # Default test key
            
            with pytest.raises(AIConfigurationError, match="Gemini API key not configured"):
                GeminiService()
    
    def test_initialization_invalid_api_key(self, mock_chat_client):
        """Test initialization failure with invalid API key."""
        with patch('app.services.gemini_service.settings') as mock_settings:
            mock_settings.model_api_key = None
            
            with pytest.raises(AIConfigurationError, match="Gemini API key not configured"):
                GeminiService()
    
    def test_message_conversion(self, mock_settings, mock_chat_client, sample_messages):
        """Test message format conversion."""
        service = GeminiService()
        langchain_messages = service._convert_messages(sample_messages)
        
        assert len(langchain_messages) == 4
        # Check that message types are converted correctly
        assert langchain_messages[0].__class__.__name__ == "SystemMessage"
        assert langchain_messages[1].__class__.__name__ == "HumanMessage"
        assert langchain_messages[2].__class__.__name__ == "AIMessage"
        assert langchain_messages[3].__class__.__name__ == "HumanMessage"
    
    @pytest.mark.asyncio
    async def test_chat_success(self, mock_settings, mock_chat_client, sample_messages):
        """Test successful chat completion."""
        # Setup mock response
        mock_response = Mock()
        mock_response.content = "This is a test response from Gemini."
        
        mock_client_instance = Mock()
        mock_client_instance.ainvoke = AsyncMock(return_value=mock_response)
        mock_chat_client.return_value = mock_client_instance
        
        service = GeminiService()
        response = await service.chat(sample_messages)
        
        assert response == "This is a test response from Gemini."
        mock_client_instance.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_chat_rate_limit_error(self, mock_settings, mock_chat_client, sample_messages):
        """Test chat with rate limit error."""
        mock_client_instance = Mock()
        mock_client_instance.ainvoke = AsyncMock(side_effect=Exception("Rate limit exceeded"))
        mock_chat_client.return_value = mock_client_instance
        
        service = GeminiService()
        
        with pytest.raises(AIRateLimitError, match="Gemini rate limit exceeded"):
            await service.chat(sample_messages)
    
    @pytest.mark.asyncio
    async def test_chat_authentication_error(self, mock_settings, mock_chat_client, sample_messages):
        """Test chat with authentication error."""
        mock_client_instance = Mock()
        mock_client_instance.ainvoke = AsyncMock(side_effect=Exception("Invalid API key"))
        mock_chat_client.return_value = mock_client_instance
        
        service = GeminiService()
        
        with pytest.raises(AIConfigurationError, match="Gemini authentication error"):
            await service.chat(sample_messages)
    
    @pytest.mark.asyncio
    async def test_chat_general_error(self, mock_settings, mock_chat_client, sample_messages):
        """Test chat with general provider error."""
        mock_client_instance = Mock()
        mock_client_instance.ainvoke = AsyncMock(side_effect=Exception("Unknown error"))
        mock_chat_client.return_value = mock_client_instance
        
        service = GeminiService()
        
        with pytest.raises(AIProviderError, match="Gemini provider error"):
            await service.chat(sample_messages)
    
    @pytest.mark.asyncio
    async def test_chat_stream_success(self, mock_settings, mock_chat_client, sample_messages):
        """Test successful streaming chat."""
        # Setup mock streaming response
        async def mock_astream(messages):
            chunks = ["Hello ", "there! ", "How ", "can ", "I ", "help?"]
            for chunk in chunks:
                mock_chunk = Mock()
                mock_chunk.content = chunk
                yield mock_chunk
        
        mock_client_instance = Mock()
        mock_client_instance.astream = mock_astream
        mock_chat_client.return_value = mock_client_instance
        
        service = GeminiService()
        
        response_chunks = []
        async for chunk in service.chat_stream(sample_messages):
            response_chunks.append(chunk)
        
        assert response_chunks == ["Hello ", "there! ", "How ", "can ", "I ", "help?"]
    
    @pytest.mark.asyncio
    async def test_chat_stream_error(self, mock_settings, mock_chat_client, sample_messages):
        """Test streaming chat with error."""
        async def mock_astream_error(messages):
            raise Exception("Streaming error")
            yield  # This will never be reached
        
        mock_client_instance = Mock()
        mock_client_instance.astream = mock_astream_error
        mock_chat_client.return_value = mock_client_instance
        
        service = GeminiService()
        
        with pytest.raises(AIProviderError, match="Gemini provider error"):
            async for chunk in service.chat_stream(sample_messages):
                pass
    
    def test_validate_configuration_success(self, mock_settings, mock_chat_client):
        """Test successful configuration validation."""
        service = GeminiService()
        assert service.validate_configuration() is True
    
    def test_validate_configuration_failure(self, mock_chat_client):
        """Test configuration validation failure."""
        with patch('app.services.gemini_service.settings') as mock_settings:
            mock_settings.model_api_key = "test-model-key"  # Default test key
            
            with pytest.raises(AIConfigurationError):
                service = GeminiService()
    
    def test_get_model_info(self, mock_settings, mock_chat_client):
        """Test model information retrieval."""
        service = GeminiService()
        info = service.get_model_info()
        
        assert info["provider"] == "google"
        assert info["model"] == "gemini-2.0-flash"
        assert info["type"] == "chat"
        assert "streaming" in info["capabilities"]
        assert info["configured"] is True


class TestAIServiceFactory:
    """Test cases for AIServiceFactory."""
    
    def setup_method(self):
        """Clear factory cache before each test."""
        AIServiceFactory.clear_cache()
    
    def test_create_service_default(self):
        """Test creating default service."""
        with patch('app.services.ai_factory.settings') as mock_settings:
            mock_settings.model_provider = "gemini"
            
            # Mock the service class directly in the factory's registry
            mock_service_class = Mock()
            mock_instance = Mock()
            mock_instance.validate_configuration.return_value = True
            mock_service_class.return_value = mock_instance
            
            # Replace the service in the factory registry
            original_services = AIServiceFactory._services.copy()
            AIServiceFactory._services["gemini"] = mock_service_class
            
            try:
                service = AIServiceFactory.create_service()
                
                assert service == mock_instance
                mock_service_class.assert_called_once()
            finally:
                # Restore original services
                AIServiceFactory._services = original_services
    
    def test_create_service_unsupported_provider(self):
        """Test creating service with unsupported provider."""
        with pytest.raises(AIConfigurationError, match="Unsupported AI provider"):
            AIServiceFactory.create_service("unsupported")
    
    def test_service_caching(self):
        """Test that services are cached properly."""
        # Mock the service class directly in the factory's registry
        mock_service_class = Mock()
        mock_instance = Mock()
        mock_instance.validate_configuration.return_value = True
        mock_service_class.return_value = mock_instance
        
        # Replace the service in the factory registry
        original_services = AIServiceFactory._services.copy()
        AIServiceFactory._services["gemini"] = mock_service_class
        
        try:
            # First call should create new instance
            service1 = AIServiceFactory.create_service("gemini")
            
            # Second call should return cached instance
            service2 = AIServiceFactory.create_service("gemini")
            
            assert service1 == service2
            mock_service_class.assert_called_once()  # Should only be called once
        finally:
            # Restore original services
            AIServiceFactory._services = original_services
    
    def test_list_providers(self):
        """Test listing available providers."""
        providers = AIServiceFactory.list_providers()
        assert "gemini" in providers
    
    def test_register_service(self):
        """Test registering new service."""
        class MockService(BaseAIService):
            async def chat(self, messages): pass
            async def chat_stream(self, messages): pass
            def validate_configuration(self): return True
            def get_model_info(self): return {}
        
        AIServiceFactory.register_service("mock", MockService)
        providers = AIServiceFactory.list_providers()
        assert "mock" in providers
    
    @patch('app.services.ai_factory.AIServiceFactory.get_default_service')
    def test_get_ai_service_convenience_function(self, mock_get_default):
        """Test convenience function for getting AI service."""
        mock_service = Mock()
        mock_get_default.return_value = mock_service
        
        service = get_ai_service()
        
        assert service == mock_service
        mock_get_default.assert_called_once() 