"""
Admin API endpoints for system status and management.
"""

import time
from datetime import datetime
from fastapi import APIRouter, Depends
from loguru import logger

from app.models import SystemStatus
from app.config import settings
from app.services.vector_search import VectorSearchService
from app.services.youtube_service import YouTubeService

router = APIRouter()


def get_vector_search() -> VectorSearchService:
    """Dependency to get vector search service."""
    from app.main import app_state
    return app_state["vector_search"]


def get_youtube_service() -> YouTubeService:
    """Dependency to get YouTube service."""
    from app.main import app_state
    return app_state["youtube_service"]


@router.get("/status", response_model=SystemStatus)
async def get_system_status(
    vector_search: VectorSearchService = Depends(get_vector_search),
    youtube_service: YouTubeService = Depends(get_youtube_service),
):
    """
    Get comprehensive system status.
    
    Returns:
    - Service health
    - Index status
    - Database connection
    - YouTube API availability
    - Uptime
    """
    from app.main import app_state
    
    start_time = app_state.get("start_time", time.time())
    uptime = time.time() - start_time
    
    # Check vector search status
    index_loaded = False
    index_size = 0
    total_videos = 0
    
    try:
        if vector_search and vector_search.index is not None:
            index_loaded = True
            index_size = vector_search.index.ntotal
            total_videos = len(vector_search.metadata) if vector_search.metadata else 0
    except Exception as e:
        logger.warning(f"Error checking vector search status: {e}")
    
    # Check YouTube API
    youtube_api_available = False
    try:
        if youtube_service:
            youtube_api_available = youtube_service.test_connection()
    except Exception as e:
        logger.warning(f"Error checking YouTube API: {e}")
    
    # Determine overall status
    if index_loaded and youtube_api_available:
        status = "healthy"
    elif index_loaded or youtube_api_available:
        status = "degraded"
    else:
        status = "unhealthy"
    
    return SystemStatus(
        status=status,
        version=settings.app_version,
        uptime_seconds=uptime,
        index_loaded=index_loaded,
        index_size=index_size,
        total_videos=total_videos,
        youtube_api_available=youtube_api_available,
        database_connected=True,  # TODO: Add actual DB check
        timestamp=datetime.utcnow(),
    )


@router.post("/reload-index")
async def reload_index(
    vector_search: VectorSearchService = Depends(get_vector_search),
):
    """
    Reload the FAISS index from disk.
    
    Use this after running the data pipeline to load updated index.
    """
    try:
        logger.info("Reloading FAISS index...")
        vector_search.load_index()
        
        return {
            "status": "success",
            "message": "Index reloaded successfully",
            "index_size": vector_search.index.ntotal if vector_search.index else 0,
        }
    except Exception as e:
        logger.error(f"Error reloading index: {e}")
        return {
            "status": "error",
            "message": f"Failed to reload index: {str(e)}",
        }


@router.get("/logs")
async def get_recent_logs(lines: int = 100):
    """
    Get recent application logs.
    
    - **lines**: Number of log lines to return (default: 100)
    """
    try:
        # TODO: Implement log reading
        return {
            "status": "success",
            "logs": [],
            "message": "Log retrieval not yet implemented",
        }
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return {
            "status": "error",
            "message": f"Failed to read logs: {str(e)}",
        }
