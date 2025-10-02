"""
Data ingestion API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from loguru import logger

from app.models import (
    IngestCollectRequest,
    IngestCollectResponse,
    IngestTranscriptsRequest,
    IngestTranscriptsResponse,
    IndexEmbedRequest,
    IndexEmbedResponse,
)
from app.services.youtube_service import YouTubeService
from app.services.vector_search import VectorSearchService

router = APIRouter()


def get_youtube_service() -> YouTubeService:
    """Dependency to get YouTube service."""
    from app.main import app_state
    if app_state["youtube_service"] is None:
        raise HTTPException(status_code=503, detail="YouTube service not initialized")
    return app_state["youtube_service"]


def get_vector_search() -> VectorSearchService:
    """Dependency to get vector search service."""
    from app.main import app_state
    if app_state["vector_search"] is None:
        raise HTTPException(status_code=503, detail="Vector search service not initialized")
    return app_state["vector_search"]


@router.post("/collect", response_model=IngestCollectResponse)
async def collect_videos(
    request: IngestCollectRequest,
    background_tasks: BackgroundTasks,
    youtube_service: YouTubeService = Depends(get_youtube_service),
):
    """
    Collect videos from YouTube using Data API.
    
    Provide one of:
    - **channel_id**: YouTube channel ID
    - **channel_url**: YouTube channel URL
    - **playlist_id**: YouTube playlist ID
    - **video_ids**: List of specific video IDs
    """
    try:
        logger.info(f"Starting video collection: {request.model_dump()}")
        
        # Validate input
        if not any([request.channel_id, request.channel_url, request.playlist_id, request.video_ids]):
            raise HTTPException(
                status_code=400,
                detail="Must provide channel_id, channel_url, playlist_id, or video_ids",
            )
        
        # Run collection (synchronously for now, can be made async)
        videos_collected = youtube_service.collect_videos(
            channel_id=request.channel_id,
            channel_url=request.channel_url,
            playlist_id=request.playlist_id,
            video_ids=request.video_ids,
            max_results=request.max_results,
            published_after=request.published_after,
        )
        
        logger.info(f"Collected {videos_collected} videos")
        
        return IngestCollectResponse(
            status="success",
            videos_collected=videos_collected,
            message=f"Successfully collected {videos_collected} videos",
        )
        
    except Exception as e:
        logger.error(f"Video collection error: {e}")
        raise HTTPException(status_code=500, detail=f"Collection failed: {str(e)}")


@router.post("/transcripts", response_model=IngestTranscriptsResponse)
async def fetch_transcripts(
    request: IngestTranscriptsRequest,
    background_tasks: BackgroundTasks,
    youtube_service: YouTubeService = Depends(get_youtube_service),
):
    """
    Fetch transcripts for collected videos.
    
    - **video_ids**: Specific video IDs (optional, default: all videos without transcripts)
    - **force_refresh**: Re-fetch existing transcripts
    """
    try:
        logger.info(f"Starting transcript fetching: {request.model_dump()}")
        
        success_count, failed_count = youtube_service.fetch_transcripts(
            video_ids=request.video_ids,
            force_refresh=request.force_refresh,
        )
        
        logger.info(f"Fetched {success_count} transcripts, {failed_count} failed")
        
        return IngestTranscriptsResponse(
            status="success" if failed_count == 0 else "partial",
            transcripts_fetched=success_count,
            transcripts_failed=failed_count,
            message=f"Fetched {success_count} transcripts ({failed_count} failed)",
        )
        
    except Exception as e:
        logger.error(f"Transcript fetching error: {e}")
        raise HTTPException(status_code=500, detail=f"Transcript fetching failed: {str(e)}")


@router.post("/embed", response_model=IndexEmbedResponse)
async def create_embeddings_and_index(
    request: IndexEmbedRequest,
    background_tasks: BackgroundTasks,
    vector_search: VectorSearchService = Depends(get_vector_search),
):
    """
    Generate embeddings and build FAISS index.
    
    - **model_name**: Embedding model (optional, uses config default)
    - **batch_size**: Batch size for embedding generation
    - **force_rebuild**: Rebuild existing index
    """
    try:
        logger.info(f"Starting embedding and indexing: {request.model_dump()}")
        
        videos_indexed, index_size = vector_search.build_index(
            model_name=request.model_name,
            batch_size=request.batch_size,
            force_rebuild=request.force_rebuild,
        )
        
        logger.info(f"Indexed {videos_indexed} videos, index size: {index_size}")
        
        return IndexEmbedResponse(
            status="success",
            videos_indexed=videos_indexed,
            index_size=index_size,
            message=f"Successfully indexed {videos_indexed} videos",
        )
        
    except Exception as e:
        logger.error(f"Embedding and indexing error: {e}")
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")
