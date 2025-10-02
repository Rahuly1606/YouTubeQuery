"""
Pydantic models for API request/response schemas.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


# ==================== Search Models ====================


class SearchRequest(BaseModel):
    """Search request payload."""

    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    metric: str = Field(default="cosine", description="Distance metric (cosine, euclidean, dot_product)")
    min_score: Optional[float] = Field(default=None, ge=0, le=1, description="Minimum similarity score")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Additional filters")

    @validator("metric")
    def validate_metric(cls, v):
        allowed_metrics = ["cosine", "euclidean", "dot_product"]
        if v not in allowed_metrics:
            raise ValueError(f"Metric must be one of {allowed_metrics}")
        return v


class TranscriptSegment(BaseModel):
    """A segment of video transcript with timestamp."""

    text: str = Field(..., description="Transcript text")
    start: float = Field(..., description="Start time in seconds")
    duration: float = Field(..., description="Duration in seconds")


class SearchResult(BaseModel):
    """Single search result."""

    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    channel: str = Field(..., description="Channel name")
    channel_id: str = Field(..., description="Channel ID")
    published_at: str = Field(..., description="Publication date")
    thumbnail_url: str = Field(..., description="Thumbnail URL")
    description: Optional[str] = Field(None, description="Video description")
    score: float = Field(..., ge=0, le=1, description="Similarity score")
    snippet: Optional[str] = Field(None, description="Relevant transcript snippet")
    start_time: Optional[float] = Field(None, description="Snippet start time in seconds")
    view_count: Optional[int] = Field(None, description="View count")
    duration: Optional[str] = Field(None, description="Video duration")


class SearchResponse(BaseModel):
    """Search results response."""

    query: str = Field(..., description="Original search query")
    results: List[SearchResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")
    took_ms: float = Field(..., description="Query execution time in milliseconds")


# ==================== Video Models ====================


class VideoDetail(BaseModel):
    """Detailed video information."""

    video_id: str
    title: str
    channel: str
    channel_id: str
    published_at: str
    thumbnail_url: str
    description: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    duration: Optional[str] = None
    tags: Optional[List[str]] = None
    transcript: Optional[List[TranscriptSegment]] = None


# ==================== Ingestion Models ====================


class IngestCollectRequest(BaseModel):
    """Request to collect videos from YouTube."""

    channel_id: Optional[str] = Field(None, description="YouTube channel ID")
    channel_url: Optional[str] = Field(None, description="YouTube channel URL")
    playlist_id: Optional[str] = Field(None, description="YouTube playlist ID")
    video_ids: Optional[List[str]] = Field(None, description="Specific video IDs to collect")
    max_results: int = Field(default=100, ge=1, le=500, description="Maximum videos to collect")
    published_after: Optional[str] = Field(None, description="ISO 8601 date string")


class IngestCollectResponse(BaseModel):
    """Response from video collection."""

    status: str = Field(..., description="Status (success, failed, partial)")
    videos_collected: int = Field(..., description="Number of videos collected")
    message: str = Field(..., description="Status message")
    job_id: Optional[str] = Field(None, description="Background job ID if async")


class IngestTranscriptsRequest(BaseModel):
    """Request to fetch transcripts."""

    video_ids: Optional[List[str]] = Field(None, description="Specific video IDs (default: all)")
    force_refresh: bool = Field(default=False, description="Re-fetch existing transcripts")


class IngestTranscriptsResponse(BaseModel):
    """Response from transcript fetching."""

    status: str
    transcripts_fetched: int
    transcripts_failed: int
    message: str
    job_id: Optional[str] = None


class IndexEmbedRequest(BaseModel):
    """Request to create embeddings and index."""

    model_name: Optional[str] = Field(None, description="Embedding model to use")
    batch_size: Optional[int] = Field(None, ge=1, le=256, description="Batch size for embedding")
    force_rebuild: bool = Field(default=False, description="Rebuild existing index")


class IndexEmbedResponse(BaseModel):
    """Response from embedding and indexing."""

    status: str
    videos_indexed: int
    index_size: int
    message: str
    job_id: Optional[str] = None


# ==================== Status Models ====================


class JobStatus(BaseModel):
    """Background job status."""

    job_id: str
    status: str = Field(..., description="Status (pending, running, completed, failed)")
    progress: Optional[float] = Field(None, ge=0, le=100, description="Progress percentage")
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None


class SystemStatus(BaseModel):
    """System health and status."""

    status: str = Field(..., description="Overall status (healthy, degraded, unhealthy)")
    version: str
    uptime_seconds: float
    index_loaded: bool
    index_size: int
    total_videos: int
    youtube_api_available: bool
    database_connected: bool
    timestamp: datetime


# ==================== Error Models ====================


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==================== Health Check ====================


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
