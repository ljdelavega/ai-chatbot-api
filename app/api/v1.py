"""
API v1 router containing all version 1 endpoints.

This module defines the API routes for version 1 of the chat API.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.api.models import HealthResponse, ChatRequest, ChatResponse
from app.api.auth import get_api_key
from app.services.ai_factory import AIServiceFactory
from app.services.ai_service import AIServiceError, AIProviderError, AIConfigurationError, AIRateLimitError
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create API router
router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the API service"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint that returns the current status of the API.
    
    This endpoint is excluded from authentication and can be used
    for monitoring and load balancer health checks.
    
    Returns:
        HealthResponse: Current service status, timestamp, and version
    """
    logger.debug("Health check endpoint accessed")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="0.1.0"
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI",
    description="Send a message to the AI and receive a response"
)
async def chat(request: ChatRequest, api_key: str = Depends(get_api_key)) -> ChatResponse:
    """
    Chat endpoint that processes a conversation and returns an AI response.
    
    This endpoint accepts a list of messages representing the conversation history
    and returns the AI's response. The endpoint requires authentication via X-API-Key header.
    
    Args:
        request: ChatRequest containing the message history
        
    Returns:
        ChatResponse: The AI's response to the conversation
        
    Raises:
        HTTPException: Various error conditions with appropriate status codes
    """
    try:
        logger.info(f"Processing chat request with {len(request.messages)} messages")
        
        # Get AI service from factory
        ai_service = AIServiceFactory.get_default_service()
        
        # Process the chat request
        response_content = await ai_service.chat(request.messages)
        
        logger.info("Chat request processed successfully")
        
        return ChatResponse(
            content=response_content,
            model=ai_service.model_name
        )
        
    except AIRateLimitError as e:
        logger.warning(f"Rate limit exceeded: {str(e)}")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {str(e)}"
        )
        
    except AIConfigurationError as e:
        logger.error(f"AI service configuration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="AI service configuration error"
        )
        
    except AIProviderError as e:
        logger.error(f"AI provider error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"AI provider error: {str(e)}"
        )
        
    except AIServiceError as e:
        logger.error(f"AI service error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.post(
    "/chat/stream",
    summary="Streaming Chat with AI",
    description="Send a message to the AI and receive a streaming response"
)
async def chat_stream(request: ChatRequest, api_key: str = Depends(get_api_key)):
    """
    Streaming chat endpoint that processes a conversation and returns a streaming AI response.
    
    This endpoint accepts a list of messages representing the conversation history
    and returns the AI's response as a stream of text chunks. The endpoint requires 
    authentication via X-API-Key header.
    
    Args:
        request: ChatRequest containing the message history
        
    Returns:
        StreamingResponse: Real-time streaming AI response
        
    Raises:
        HTTPException: Various error conditions with appropriate status codes
    """
    async def generate_response():
        try:
            logger.info(f"Processing streaming chat request with {len(request.messages)} messages")
            
            # Get AI service from factory
            ai_service = AIServiceFactory.get_default_service()
            
            # Stream the response
            async for chunk in ai_service.chat_stream(request.messages):
                yield f"data: {chunk}\n\n"
            
            logger.info("Streaming chat request completed successfully")
            
        except AIRateLimitError as e:
            logger.warning(f"Rate limit exceeded during streaming: {str(e)}")
            yield f"event: error\ndata: Rate limit exceeded: {str(e)}\n\n"
            
        except AIConfigurationError as e:
            logger.error(f"AI service configuration error during streaming: {str(e)}")
            yield f"event: error\ndata: AI service configuration error\n\n"
            
        except AIProviderError as e:
            logger.error(f"AI provider error during streaming: {str(e)}")
            yield f"event: error\ndata: AI provider error: {str(e)}\n\n"
            
        except AIServiceError as e:
            logger.error(f"AI service error during streaming: {str(e)}")
            yield f"event: error\ndata: AI service error: {str(e)}\n\n"
            
        except Exception as e:
            logger.error(f"Unexpected error in streaming chat endpoint: {str(e)}")
            yield f"event: error\ndata: Internal server error\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )