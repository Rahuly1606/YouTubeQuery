"""
Video detail API endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from app.models import VideoDetail, TranscriptSegment
from app.services.youtube_service import YouTubeService

router = APIRouter()


def get_youtube_service() -> YouTubeService:
    """Dependency to get YouTube service."""
    from app.main import app_state
    if app_state["youtube_service"] is None:
        raise HTTPException(status_code=503, detail="YouTube service not initialized")
    return app_state["youtube_service"]


@router.get("/{video_id}", response_model=VideoDetail)
async def get_video_details(
    video_id: str,
    youtube_service: YouTubeService = Depends(get_youtube_service),
):
    """
    Get detailed information about a specific video.
    
    - **video_id**: YouTube video ID
    
    Returns video metadata and full transcript if available.
    """
    try:
        logger.info(f"Fetching details for video: {video_id}")
        
        video_data = youtube_service.get_video_details(video_id)
        
        if not video_data:
            raise HTTPException(status_code=404, detail=f"Video not found: {video_id}")
        
        # Convert transcript to TranscriptSegment models
        transcript = None
        if video_data.get("transcript"):
            transcript = [
                TranscriptSegment(
                    text=segment["text"],
                    start=segment["start"],
                    duration=segment["duration"],
                )
                for segment in video_data["transcript"]
            ]
        
        return VideoDetail(
            video_id=video_data["video_id"],
            title=video_data["title"],
            channel=video_data["channel"],
            channel_id=video_data.get("channel_id", ""),
            published_at=video_data.get("published_at", ""),
            thumbnail_url=video_data.get("thumbnail_url", ""),
            description=video_data.get("description"),
            view_count=video_data.get("view_count"),
            like_count=video_data.get("like_count"),
            duration=video_data.get("duration"),
            tags=video_data.get("tags"),
            transcript=transcript,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching video details: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch video: {str(e)}")


@router.get("/{video_id}/transcript")
async def get_video_transcript(
    video_id: str,
    youtube_service: YouTubeService = Depends(get_youtube_service),
):
    """
    Get only the transcript for a video.
    
    - **video_id**: YouTube video ID
    """
    try:
        transcript = youtube_service.get_transcript(video_id)
        
        if transcript is None:
            raise HTTPException(
                status_code=404,
                detail=f"Transcript not available for video: {video_id}",
            )
        
        return {
            "video_id": video_id,
            "transcript": transcript,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching transcript: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch transcript: {str(e)}")
