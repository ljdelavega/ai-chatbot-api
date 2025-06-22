"""
Main application entry point for the AI Chatbot API.

This module creates and configures the FastAPI application instance.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1 import router as v1_router
from app.api.models import ErrorResponse

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(v1_router)


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and return structured error responses."""
    logger.warning(f"HTTP {exc.status_code} error on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    logger.error(f"ValueError on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid input: {str(exc)}"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
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