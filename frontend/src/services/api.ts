/**
 * API client for QueryTube backend
 */

import type { SearchRequest, SearchResponse, VideoDetail } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Search for videos using semantic search
 */
export async function searchVideos(request: SearchRequest): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Get video details by ID
 */
export async function getVideo(videoId: string): Promise<VideoDetail> {
    const response = await fetch(`${API_BASE_URL}/api/video/${videoId}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch video: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Check backend health status
 */
export async function checkHealth(): Promise<{ status: string; timestamp: string }> {
    const response = await fetch(`${API_BASE_URL}/api/health`);

    if (!response.ok) {
        throw new Error(`Health check failed: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Trigger video collection from YouTube
 */
export async function collectVideos(params: {
    channel_id?: string;
    playlist_id?: string;
    max_results?: number;
}): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/ingest/collect`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    });

    if (!response.ok) {
        throw new Error(`Collection failed: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Trigger transcript fetching
 */
export async function fetchTranscripts(params: {
    video_ids?: string[];
    force_refresh?: boolean;
}): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/ingest/transcripts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    });

    if (!response.ok) {
        throw new Error(`Transcript fetch failed: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Trigger index building
 */
export async function buildIndex(params: {
    model_name?: string;
    force_rebuild?: boolean;
}): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/index/embed`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    });

    if (!response.ok) {
        throw new Error(`Index build failed: ${response.statusText}`);
    }

    return response.json();
}
