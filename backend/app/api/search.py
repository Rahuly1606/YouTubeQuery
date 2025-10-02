"""
Search API endpoints.
"""

import time
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from loguru import logger

from app.models import SearchRequest, SearchResponse, SearchResult
from app.services.vector_search import VectorSearchService

router = APIRouter()


def get_vector_search() -> VectorSearchService:
    """Dependency to get vector search service."""
    from app.main import app_state
    if app_state["vector_search"] is None:
        raise HTTPException(status_code=503, detail="Vector search service not initialized")
    return app_state["vector_search"]


@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    vector_search: VectorSearchService = Depends(get_vector_search),
):
    """
    Perform semantic search across YouTube videos.
    
    - **query**: Search query text
    - **top_k**: Number of results to return (1-50)
    - **metric**: Distance metric (cosine, euclidean, dot_product)
    - **min_score**: Minimum similarity score threshold (0-1)
    """
    start_time = time.time()
    
    try:
        logger.info(f"Search query: '{request.query}' (top_k={request.top_k})")
        
        # Perform vector search
        results = vector_search.search(
            query=request.query,
            top_k=request.top_k,
            metric=request.metric,
            min_score=request.min_score,
        )
        
        # Convert to SearchResult models
        search_results = [
            SearchResult(
                video_id=r["video_id"],
                title=r["title"],
                channel=r["channel"],
                channel_id=r.get("channel_id", ""),
                published_at=r.get("published_at", ""),
                thumbnail_url=r.get("thumbnail_url", ""),
                description=r.get("description"),
                score=r["score"],
                snippet=r.get("snippet"),
                start_time=r.get("start_time"),
                view_count=r.get("view_count"),
                duration=r.get("duration"),
            )
            for r in results
        ]
        
        took_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Found {len(search_results)} results in {took_ms:.2f}ms")
        
        return SearchResponse(
            query=request.query,
            results=search_results,
            total=len(search_results),
            took_ms=took_ms,
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search", response_model=SearchResponse)
async def search_get(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    top_k: int = Query(default=5, ge=1, le=50, description="Number of results"),
    metric: str = Query(default="cosine", description="Distance metric"),
    min_score: Optional[float] = Query(default=None, ge=0, le=1, description="Minimum score"),
    vector_search: VectorSearchService = Depends(get_vector_search),
):
    """
    GET version of search endpoint for simple queries.
    
    Example: GET /api/search?q=machine+learning&top_k=10
    """
    request = SearchRequest(
        query=q,
        top_k=top_k,
        metric=metric,
        min_score=min_score,
    )
    return await search(request, vector_search)


@router.get("/autocomplete")
async def autocomplete(
    q: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(default=10, ge=1, le=20),
):
    """
    Autocomplete suggestions for search queries.
    
    Returns popular/recent queries that match the input.
    """
    # TODO: Implement autocomplete using query history
    # For now, return empty suggestions
    return {
        "query": q,
        "suggestions": [],
    }
