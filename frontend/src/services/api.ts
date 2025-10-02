/**
 * API Service Functions
 * 
 * All API calls to the QueryTube backend.
 */

import apiClient from '@/lib/api';
import {
    SearchRequest,
    SearchResponse,
    VideoDetail,
    SystemStatus,
    IngestCollectRequest,
    IngestCollectResponse,
    IngestTranscriptsRequest,
    IngestTranscriptsResponse,
    IndexEmbedRequest,
    IndexEmbedResponse,
} from '@/types';

// ==================== Search ====================

export async function searchVideos(request: SearchRequest): Promise<SearchResponse> {
    const response = await apiClient.post<SearchResponse>('/api/search', request);
    return response.data;
}

export async function searchVideosGet(query: string, topK: number = 5): Promise<SearchResponse> {
    const response = await apiClient.get<SearchResponse>('/api/search', {
        params: { q: query, top_k: topK },
    });
    return response.data;
}

export async function getAutocomplete(query: string, limit: number = 10): Promise<string[]> {
    const response = await apiClient.get('/api/autocomplete', {
        params: { q: query, limit },
    });
    return response.data.suggestions || [];
}

// ==================== Video Details ====================

export async function getVideoDetail(videoId: string): Promise<VideoDetail> {
    const response = await apiClient.get<VideoDetail>(`/api/video/${videoId}`);
    return response.data;
}

export async function getVideoTranscript(videoId: string): Promise<any> {
    const response = await apiClient.get(`/api/video/${videoId}/transcript`);
    return response.data;
}

// ==================== Admin ====================

export async function getSystemStatus(): Promise<SystemStatus> {
    const response = await apiClient.get<SystemStatus>('/api/admin/status');
    return response.data;
}

export async function reloadIndex(): Promise<any> {
    const response = await apiClient.post('/api/admin/reload-index');
    return response.data;
}

// ==================== Ingestion ====================

export async function collectVideos(request: IngestCollectRequest): Promise<IngestCollectResponse> {
    const response = await apiClient.post<IngestCollectResponse>('/api/ingest/collect', request);
    return response.data;
}

export async function fetchTranscripts(
    request: IngestTranscriptsRequest
): Promise<IngestTranscriptsResponse> {
    const response = await apiClient.post<IngestTranscriptsResponse>('/api/ingest/transcripts', request);
    return response.data;
}

export async function createEmbeddings(request: IndexEmbedRequest): Promise<IndexEmbedResponse> {
    const response = await apiClient.post<IndexEmbedResponse>('/api/ingest/embed', request);
    return response.data;
}

// ==================== Health ====================

export async function checkHealth(): Promise<{ status: string }> {
    const response = await apiClient.get('/health');
    return response.data;
}
