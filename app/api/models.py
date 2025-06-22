"""
Pydantic models for API requests and responses.

This module defines the data models used for validating API inputs
and structuring API outputs.
"""

from typing import List, Literal
from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in a chat conversation."""
    
    role: Literal["system", "user", "assistant"] = Field(
        ...,
        description="The role of the message sender"
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,  # Will be configurable via settings
        description="The content of the message"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello, how are you today?"
            }
        }


class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    
    messages: List[Message] = Field(
        ...,
        min_length=1,
        max_length=50,  # Will be configurable via settings
        description="List of messages in the conversation history"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": "Hello, how are you?"
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""
    
    status: str = Field(
        ...,
        description="Health status of the service"
    )
    timestamp: datetime = Field(
        ...,
        description="Current server timestamp"
    )
    version: str = Field(
        ...,
        description="API version"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-01-21T10:30:00Z",
                "version": "0.1.0"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    detail: str = Field(
        ...,
        description="Error message describing what went wrong"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid API key provided"
            }
        } 