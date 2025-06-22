"""
Configuration management using Pydantic BaseSettings.

This module handles all environment variable loading and validation
for the AI Chatbot API.
"""

from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",  # Load environment variables from .env file
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # API Configuration
    api_key: str = Field(
        default="test-api-key", 
        description="Static API key for endpoint protection",
        alias="API_KEY"
    )
    
    # AI Model Configuration
    model_provider: str = Field(
        default="gemini", 
        description="AI provider (gemini, openai, anthropic)",
        alias="MODEL_PROVIDER"
    )
    model_api_key: str = Field(
        default="test-model-key", 
        description="API key for the AI model provider",
        alias="MODEL_API_KEY"
    )
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["*"], 
        description="Allowed CORS origins (comma-separated)",
        alias="ALLOWED_ORIGINS"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO", 
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
        alias="LOG_LEVEL"
    )
    
    # Server Configuration
    host: str = Field(
        default="0.0.0.0", 
        description="Server host",
        alias="HOST"
    )
    port: int = Field(
        default=8000, 
        description="Server port",
        alias="PORT"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(
        default=100, 
        description="Requests per minute per API key",
        alias="RATE_LIMIT_REQUESTS"
    )
    
    # Message Validation
    max_message_length: int = Field(
        default=10000, 
        description="Maximum length for a single message",
        alias="MAX_MESSAGE_LENGTH"
    )
    max_history_length: int = Field(
        default=50, 
        description="Maximum number of messages in history",
        alias="MAX_HISTORY_LENGTH"
    )

    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse comma-separated origins or JSON array into a list."""
        if isinstance(v, str):
            # Handle empty string case
            if not v.strip():
                return ["*"]
            # Try JSON parsing first (for ["url1","url2"] format)
            try:
                import json
                return json.loads(v)
            except (json.JSONDecodeError, ValueError):
                # Fall back to comma-separated parsing
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif v is None:
            return ["*"]
        return v


# Global settings instance
settings = Settings() 