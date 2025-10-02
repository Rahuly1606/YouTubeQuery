/**
 * TypeScript Type Definitions
 */

export interface Video {
    video_id: string;
    title: string;
    channel: string;
    channel_id: string;
    published_at: string;
    thumbnail_url: string;
    description?: string;
    view_count?: number;
    like_count?: number;
    duration?: string;
    tags?: string[];
}

export interface TranscriptSegment {
    text: string;
    start: number;
    duration: number;
}

export interface SearchResult extends Video {
    score: number;
    snippet?: string;
    start_time?: number;
    // Alias for compatibility
    similarity_score?: number;
    channel_title?: string;
}

export interface SearchRequest {
    query: string;
    top_k?: number;
    limit?: number; // Alias for top_k
    metric?: 'cosine' | 'euclidean' | 'dot_product';
    min_score?: number;
    filters?: Record<string, any>;
}

export interface SearchResponse {
    query: string;
    results: SearchResult[];
    total: number;
    took_ms: number;
}

export interface VideoDetail extends Video {
    transcript?: TranscriptSegment[];
}

export interface SystemStatus {
    status: 'healthy' | 'degraded' | 'unhealthy';
    version: string;
    uptime_seconds: number;
    index_loaded: boolean;
    index_size: number;
    total_videos: number;
    youtube_api_available: boolean;
    database_connected: boolean;
    timestamp: string;
}

export interface IngestCollectRequest {
    channel_id?: string;
    channel_url?: string;
    playlist_id?: string;
    video_ids?: string[];
    max_results?: number;
    published_after?: string;
}

export interface IngestCollectResponse {
    status: string;
    videos_collected: number;
    message: string;
    job_id?: string;
}

export interface IngestTranscriptsRequest {
    video_ids?: string[];
    force_refresh?: boolean;
}

export interface IngestTranscriptsResponse {
    status: string;
    transcripts_fetched: number;
    transcripts_failed: number;
    message: string;
    job_id?: string;
}

export interface IndexEmbedRequest {
    model_name?: string;
    batch_size?: number;
    force_rebuild?: boolean;
}

export interface IndexEmbedResponse {
    status: string;
    videos_indexed: number;
    index_size: number;
    message: string;
    job_id?: string;
}

export interface ApiError {
    error: string;
    message: string;
    detail?: any;
    timestamp: string;
}
