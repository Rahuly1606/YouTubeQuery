#!/usr/bin/env python3
"""
YouTube Video Collection Script

Collects video metadata from YouTube using the Data API v3.
Supports collection from channels, playlists, or specific video IDs.

Usage:
    python collect_youtube.py --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --max-results 100
    python collect_youtube.py --playlist-id PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf --max-results 50
    python collect_youtube.py --video-ids dQw4w9WgXcQ jNQXAC9IVRw --output data/videos.parquet
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


def get_youtube_client(api_key: str):
    """Create YouTube API client."""
    return build("youtube", "v3", developerKey=api_key)


def fetch_channel_videos(
    youtube,
    channel_id: str,
    max_results: int = 100,
    published_after: Optional[str] = None,
) -> List[dict]:
    """Fetch all videos from a channel."""
    print(f"📺 Fetching videos from channel: {channel_id}")

    # Get channel's uploads playlist
    channel_response = youtube.channels().list(
        part="contentDetails,snippet",
        id=channel_id
    ).execute()

    if not channel_response.get("items"):
        raise ValueError(f"Channel not found: {channel_id}")

    channel_info = channel_response["items"][0]
    channel_title = channel_info["snippet"]["title"]
    uploads_playlist = channel_info["contentDetails"]["relatedPlaylists"]["uploads"]

    print(f"✓ Found channel: {channel_title}")
    print(f"📋 Fetching from uploads playlist: {uploads_playlist}")

    return fetch_playlist_videos(youtube, uploads_playlist, max_results, published_after)


def fetch_playlist_videos(
    youtube,
    playlist_id: str,
    max_results: int = 100,
    published_after: Optional[str] = None,
) -> List[dict]:
    """Fetch all videos from a playlist."""
    videos = []
    next_page_token = None

    print(f"📋 Fetching videos from playlist: {playlist_id}")

    while len(videos) < max_results:
        try:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(50, max_results - len(videos)),
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]
                video_id = snippet["resourceId"]["videoId"]

                # Filter by publish date
                if published_after and snippet["publishedAt"] < published_after:
                    continue

                videos.append({
                    "video_id": video_id,
                    "title": snippet["title"],
                    "channel": snippet["channelTitle"],
                    "channel_id": snippet["channelId"],
                    "published_at": snippet["publishedAt"],
                    "description": snippet["description"],
                    "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

            print(f"  Fetched {len(videos)} videos...")

        except HttpError as e:
            print(f"❌ Error: {e}")
            break

    print(f"✓ Collected {len(videos)} video metadata entries")

    # Enrich with detailed statistics
    if videos:
        print("🔍 Fetching detailed video statistics...")
        video_ids = [v["video_id"] for v in videos]
        detailed_videos = fetch_video_details(youtube, video_ids)

        # Merge details
        details_dict = {v["video_id"]: v for v in detailed_videos}
        for video in videos:
            details = details_dict.get(video["video_id"], {})
            video.update(details)

    return videos


def fetch_video_details(youtube, video_ids: List[str]) -> List[dict]:
    """Fetch detailed statistics for videos."""
    videos = []

    # Process in batches of 50 (API limit)
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]

        try:
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(batch),
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]
                statistics = item.get("statistics", {})
                content_details = item.get("contentDetails", {})

                videos.append({
                    "video_id": item["id"],
                    "view_count": int(statistics.get("viewCount", 0)),
                    "like_count": int(statistics.get("likeCount", 0)),
                    "comment_count": int(statistics.get("commentCount", 0)),
                    "duration": content_details.get("duration", ""),
                    "tags": snippet.get("tags", []),
                })

        except HttpError as e:
            print(f"❌ Error fetching details: {e}")

    return videos


def main():
    parser = argparse.ArgumentParser(
        description="Collect YouTube video metadata using Data API v3"
    )

    # Input sources (mutually exclusive)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--channel-id",
        help="YouTube channel ID (e.g., UC_x5XG1OV2P6uZZ5FSM9Ttw)",
    )
    source_group.add_argument(
        "--playlist-id",
        help="YouTube playlist ID",
    )
    source_group.add_argument(
        "--video-ids",
        nargs="+",
        help="Specific video IDs to collect",
    )

    # Options
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of videos to collect (default: 100)",
    )
    parser.add_argument(
        "--published-after",
        help="Only collect videos published after this date (ISO 8601 format)",
    )
    parser.add_argument(
        "--output",
        default="data/videos.parquet",
        help="Output parquet file path (default: data/videos.parquet)",
    )
    parser.add_argument(
        "--api-key",
        help="YouTube API key (or set YOUTUBE_API_KEY env var)",
    )

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "your_youtube_api_key_here":
        print("❌ Error: YouTube API key not configured")
        print("\nPlease either:")
        print("  1. Set YOUTUBE_API_KEY environment variable in .env file")
        print("  2. Use --api-key argument")
        print("\nGet your API key from: https://console.cloud.google.com/")
        sys.exit(1)

    try:
        # Create YouTube client
        youtube = get_youtube_client(api_key)

        # Collect videos based on source
        videos = []

        if args.channel_id:
            videos = fetch_channel_videos(
                youtube,
                args.channel_id,
                args.max_results,
                args.published_after,
            )

        elif args.playlist_id:
            videos = fetch_playlist_videos(
                youtube,
                args.playlist_id,
                args.max_results,
                args.published_after,
            )

        elif args.video_ids:
            print(f"🔍 Fetching details for {len(args.video_ids)} specific videos...")
            videos = fetch_video_details(youtube, args.video_ids)

        if not videos:
            print("⚠️  No videos collected")
            sys.exit(0)

        # Save to parquet
        df = pd.DataFrame(videos)

        # Create output directory
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save
        df.to_parquet(output_path, index=False)

        print(f"\n✅ Success!")
        print(f"   Collected: {len(videos)} videos")
        print(f"   Saved to: {output_path}")
        print(f"\nDataFrame info:")
        print(df.info())
        print(f"\nSample data:")
        print(df[["video_id", "title", "channel", "view_count"]].head())

    except HttpError as e:
        print(f"\n❌ YouTube API Error: {e}")
        if e.resp.status == 403:
            print("\n⚠️  This might be a quota or API key issue:")
            print("   • Check if YouTube Data API v3 is enabled")
            print("   • Verify your API key is correct")
            print("   • Check your API quota at: https://console.cloud.google.com/")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
