"""
YouTube Service

Handles YouTube Data API interactions and transcript fetching.
"""

import os
from typing import List, Dict, Any, Optional
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)
from loguru import logger

from app.config import settings


class YouTubeService:
    """Service for YouTube Data API and transcript operations."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize YouTube service.

        Args:
            api_key: YouTube Data API key (uses settings if not provided)
        """
        self.api_key = api_key or settings.youtube_api_key
        if not self.api_key or self.api_key == "your_youtube_api_key_here":
            raise ValueError(
                "YouTube API key not configured. "
                "Please set YOUTUBE_API_KEY in .env file. "
                "Get your key from: https://console.cloud.google.com/"
            )

        # Initialize YouTube API client
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        logger.info("YouTube API client initialized")

    def test_connection(self) -> bool:
        """Test YouTube API connection."""
        try:
            self.youtube.channels().list(part="id", mine=True).execute()
            return True
        except Exception as e:
            logger.warning(f"YouTube API connection test failed: {e}")
            return False

    def collect_videos(
        self,
        channel_id: Optional[str] = None,
        channel_url: Optional[str] = None,
        playlist_id: Optional[str] = None,
        video_ids: Optional[List[str]] = None,
        max_results: int = 100,
        published_after: Optional[str] = None,
    ) -> int:
        """
        Collect videos from YouTube and save to parquet.

        Args:
            channel_id: YouTube channel ID
            channel_url: YouTube channel URL (extracts ID)
            playlist_id: YouTube playlist ID
            video_ids: Specific video IDs to collect
            max_results: Maximum number of videos to collect
            published_after: ISO 8601 date string

        Returns:
            Number of videos collected
        """
        try:
            videos = []

            if video_ids:
                # Fetch specific videos
                videos = self._fetch_video_details(video_ids)

            elif channel_id or channel_url:
                # Extract channel ID from URL if needed
                if channel_url:
                    channel_id = self._extract_channel_id(channel_url)

                # Get channel's uploaded videos playlist
                channel_info = (
                    self.youtube.channels()
                    .list(part="contentDetails", id=channel_id)
                    .execute()
                )

                if not channel_info.get("items"):
                    raise ValueError(f"Channel not found: {channel_id}")

                uploads_playlist_id = (
                    channel_info["items"][0]
                    ["contentDetails"]
                    ["relatedPlaylists"]
                    ["uploads"]
                )

                # Fetch videos from uploads playlist
                videos = self._fetch_playlist_videos(
                    uploads_playlist_id,
                    max_results=max_results,
                    published_after=published_after,
                )

            elif playlist_id:
                # Fetch videos from playlist
                videos = self._fetch_playlist_videos(
                    playlist_id,
                    max_results=max_results,
                    published_after=published_after,
                )

            else:
                raise ValueError("Must provide channel_id, channel_url, playlist_id, or video_ids")

            # Save to parquet
            if videos:
                df = pd.DataFrame(videos)
                os.makedirs(os.path.dirname(settings.videos_path), exist_ok=True)
                df.to_parquet(settings.videos_path, index=False)
                logger.info(f"Saved {len(videos)} videos to {settings.videos_path}")

            return len(videos)

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error collecting videos: {e}")
            raise

    def _fetch_playlist_videos(
        self,
        playlist_id: str,
        max_results: int = 100,
        published_after: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch videos from a playlist with pagination."""
        videos = []
        next_page_token = None

        while len(videos) < max_results:
            try:
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token,
                )
                response = request.execute()

                # Extract video info
                for item in response.get("items", []):
                    snippet = item["snippet"]
                    video_id = snippet["resourceId"]["videoId"]

                    # Filter by publish date if specified
                    if published_after and snippet["publishedAt"] < published_after:
                        continue

                    videos.append(
                        {
                            "video_id": video_id,
                            "title": snippet["title"],
                            "channel": snippet["channelTitle"],
                            "channel_id": snippet["channelId"],
                            "published_at": snippet["publishedAt"],
                            "description": snippet["description"],
                            "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                        }
                    )

                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break

                logger.info(f"Fetched {len(videos)} videos so far...")

            except HttpError as e:
                logger.error(f"Error fetching playlist videos: {e}")
                break

        # Fetch additional details (view count, duration, etc.)
        if videos:
            video_ids = [v["video_id"] for v in videos]
            detailed_videos = self._fetch_video_details(video_ids)

            # Merge details
            details_dict = {v["video_id"]: v for v in detailed_videos}
            for video in videos:
                details = details_dict.get(video["video_id"], {})
                video.update(details)

        return videos

    def _fetch_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """Fetch detailed information for specific videos."""
        videos = []

        # Process in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]

            try:
                request = self.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=",".join(batch),
                )
                response = request.execute()

                for item in response.get("items", []):
                    snippet = item["snippet"]
                    statistics = item.get("statistics", {})
                    content_details = item.get("contentDetails", {})

                    videos.append(
                        {
                            "video_id": item["id"],
                            "title": snippet["title"],
                            "channel": snippet["channelTitle"],
                            "channel_id": snippet["channelId"],
                            "published_at": snippet["publishedAt"],
                            "description": snippet["description"],
                            "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                            "view_count": int(statistics.get("viewCount", 0)),
                            "like_count": int(statistics.get("likeCount", 0)),
                            "duration": content_details.get("duration", ""),
                            "tags": snippet.get("tags", []),
                        }
                    )

            except HttpError as e:
                logger.error(f"Error fetching video details: {e}")

        return videos

    def fetch_transcripts(
        self,
        video_ids: Optional[List[str]] = None,
        force_refresh: bool = False,
    ) -> tuple[int, int]:
        """
        Fetch transcripts for videos.

        Args:
            video_ids: Specific video IDs (default: all from videos.parquet)
            force_refresh: Re-fetch existing transcripts

        Returns:
            Tuple of (success_count, failed_count)
        """
        try:
            # Load videos
            if not os.path.exists(settings.videos_path):
                raise FileNotFoundError(
                    f"Videos file not found: {settings.videos_path}. "
                    "Please run video collection first."
                )

            df = pd.read_parquet(settings.videos_path)

            # Filter videos
            if video_ids:
                df = df[df["video_id"].isin(video_ids)]

            # Skip videos with existing transcripts unless force_refresh
            if not force_refresh and "transcript" in df.columns:
                df = df[df["transcript"].isna() | (df["transcript"] == "")]

            logger.info(f"Fetching transcripts for {len(df)} videos")

            # Fetch transcripts
            success_count = 0
            failed_count = 0
            transcripts = []

            for idx, row in df.iterrows():
                video_id = row["video_id"]
                transcript = self.get_transcript(video_id)

                if transcript:
                    # Combine transcript segments into single text
                    transcript_text = " ".join([seg["text"] for seg in transcript])
                    transcripts.append(
                        {
                            "video_id": video_id,
                            "transcript": transcript_text,
                            "transcript_segments": transcript,
                        }
                    )
                    success_count += 1
                else:
                    transcripts.append({"video_id": video_id, "transcript": None})
                    failed_count += 1

                if (success_count + failed_count) % 10 == 0:
                    logger.info(f"Progress: {success_count} success, {failed_count} failed")

            # Merge transcripts with original data
            transcript_df = pd.DataFrame(transcripts)
            result_df = df.merge(transcript_df, on="video_id", how="left", suffixes=("", "_new"))

            # Update transcript column
            if "transcript_new" in result_df.columns:
                result_df["transcript"] = result_df["transcript_new"].fillna(
                    result_df.get("transcript", "")
                )
                result_df = result_df.drop(columns=["transcript_new"])

            # Save to transcripts file
            os.makedirs(os.path.dirname(settings.transcripts_path), exist_ok=True)
            result_df.to_parquet(settings.transcripts_path, index=False)

            logger.info(f"✓ Transcript fetching complete: {success_count} success, {failed_count} failed")
            return success_count, failed_count

        except Exception as e:
            logger.error(f"Error fetching transcripts: {e}")
            raise

    def get_transcript(self, video_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get transcript for a single video.

        Args:
            video_id: YouTube video ID

        Returns:
            List of transcript segments or None if unavailable
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript_list

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            logger.debug(f"Transcript not available for {video_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching transcript for {video_id}: {e}")
            return None

    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a single video."""
        try:
            # Check if video exists in local data
            if os.path.exists(settings.transcripts_path):
                df = pd.read_parquet(settings.transcripts_path)
                row = df[df["video_id"] == video_id]

                if not row.empty:
                    video_data = row.iloc[0].to_dict()

                    # Get transcript segments if available
                    if pd.notna(video_data.get("transcript")):
                        video_data["transcript"] = self.get_transcript(video_id)

                    return video_data

            # Fallback: fetch from YouTube API
            videos = self._fetch_video_details([video_id])
            if videos:
                video_data = videos[0]
                video_data["transcript"] = self.get_transcript(video_id)
                return video_data

            return None

        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return None

    def _extract_channel_id(self, channel_url: str) -> str:
        """Extract channel ID from YouTube URL."""
        # TODO: Implement URL parsing
        # For now, assume it's already a channel ID
        return channel_url.split("/")[-1]
