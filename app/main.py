"""
Main application entry point for the AI Chatbot API.

This module creates and configures the FastAPI application instance.
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging, get_logger

# Set up logging first
setup_logging()
logger = get_logger(__name__)

# Create FastAPI application instance
app = FastAPI(
    title="AI Chatbot API",
    description="A headless, portable AI chat API service for conversational AI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Starting AI Chatbot API...")
    logger.info(f"Configuration: Provider={settings.model_provider}, Log Level={settings.log_level}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Shutting down AI Chatbot API...")


# Basic root endpoint for testing
@app.get("/")
async def root():
    """Root endpoint returning basic API information."""
    return {
        "message": "AI Chatbot API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        reload=True,  # Enable auto-reload for development
    ) 