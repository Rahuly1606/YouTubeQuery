"""
QueryTube FastAPI Application

Main application entry point with middleware, CORS, and route registration.
"""

import time
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

from app.config import settings
from app.models import HealthResponse, ErrorResponse
from app.api import search, ingest, video, admin

# Configure logging
logger.add(
    "logs/querytube_{time}.log",
    rotation="500 MB",
    retention="10 days",
    level=settings.log_level,
)

# Global state
app_state: Dict[str, Any] = {
    "start_time": time.time(),
    "vector_search": None,
    "youtube_service": None,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    logger.info("🚀 Starting QueryTube API...")
    
    # Startup
    try:
        # Initialize services
        from app.services.vector_search import VectorSearchService
        from app.services.youtube_service import YouTubeService
        
        logger.info("Initializing YouTube service...")
        app_state["youtube_service"] = YouTubeService()
        
        logger.info(f"Initializing vector search with model: {settings.embedding_model}")
        app_state["vector_search"] = VectorSearchService(
            model_name=settings.embedding_model,
            index_path=settings.index_path,
            embeddings_path=settings.embeddings_path,
        )
        
        # Try to load existing index
        try:
            app_state["vector_search"].load_index()
            logger.info("✓ Loaded existing FAISS index")
        except FileNotFoundError:
            logger.warning("⚠ No existing index found. Please run data ingestion pipeline.")
        except Exception as e:
            logger.error(f"✗ Error loading index: {e}")
        
        logger.info("✓ QueryTube API started successfully")
        
    except Exception as e:
        logger.error(f"✗ Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down QueryTube API...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Semantic search engine for YouTube videos using vector embeddings",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to all responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="ValidationError",
            message="Invalid request data",
            detail={"errors": exc.errors()},
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            detail={"type": type(exc).__name__, "message": str(exc)},
        ).model_dump(),
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


# Include routers
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(video.router, prefix="/api/video", tags=["Video"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


# Dependency to get services
def get_vector_search():
    """Get vector search service instance."""
    return app_state["vector_search"]


def get_youtube_service():
    """Get YouTube service instance."""
    return app_state["youtube_service"]
