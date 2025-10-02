#!/usr/bin/env python3
"""
Alternative YouTube Transcript Fetching Script using yt-dlp

This uses yt-dlp which is more reliable for fetching subtitles.
Works better than youtube-transcript-api when facing rate limits.

Usage:
    python get_transcripts_alternative.py
    python get_transcripts_alternative.py --delay 3.0
"""
import argparse
import sys
import time
import json
from pathlib import Path
from typing import Optional
import pandas as pd
from tqdm import tqdm

try:
    import yt_dlp
except ImportError:
    print("❌ Error: yt-dlp not installed")
    print("   Install it with: pip install yt-dlp")
    sys.exit(1)


def fetch_transcript_ytdlp(video_id: str) -> Optional[dict]:
    """
    Fetch transcript using yt-dlp (more reliable).
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with transcript text, or None if unavailable
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Try to get subtitles
            subtitles = info.get('subtitles', {})
            automatic_captions = info.get('automatic_captions', {})
            
            # Prefer manual subtitles
            if 'en' in subtitles:
                subtitle_data = subtitles['en']
            elif 'en' in automatic_captions:
                subtitle_data = automatic_captions['en']
            else:
                return {
                    "transcript": None,
                    "transcript_available": False,
                    "error": "No English subtitles available"
                }
            
            # Find JSON3 format (has text data)
            json3_sub = None
            for sub in subtitle_data:
                if sub.get('ext') == 'json3':
                    json3_sub = sub
                    break
            
            if not json3_sub:
                return {
                    "transcript": None,
                    "transcript_available": False,
                    "error": "No JSON subtitle format available"
                }
            
            # Download subtitle data
            sub_url = json3_sub['url']
            import urllib.request
            with urllib.request.urlopen(sub_url) as response:
                sub_data = json.loads(response.read().decode('utf-8'))
            
            # Extract text from events
            texts = []
            for event in sub_data.get('events', []):
                if 'segs' in event:
                    for seg in event['segs']:
                        if 'utf8' in seg:
                            texts.append(seg['utf8'])
            
            full_text = ' '.join(texts).strip()
            
            if not full_text:
                return {
                    "transcript": None,
                    "transcript_available": False,
                    "error": "Empty transcript"
                }
            
            return {
                "transcript": full_text,
                "transcript_available": True,
                "is_generated": 'en' in automatic_captions,
                "error": None
            }
            
    except Exception as e:
        return {
            "transcript": None,
            "transcript_available": False,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube video transcripts using yt-dlp (more reliable)"
    )

    parser.add_argument(
        "--input",
        default="data/videos.parquet",
        help="Input parquet file with video metadata",
    )
    parser.add_argument(
        "--output",
        default="data/transcripts.parquet",
        help="Output parquet file",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between requests in seconds (default: 2.0)",
    )

    args = parser.parse_args()

    try:
        # Load videos
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Error: Input file not found: {input_path}")
            sys.exit(1)

        print(f"📂 Loading videos from: {input_path}")
        df = pd.read_parquet(input_path)
        print(f"✓ Loaded {len(df)} videos")

        print(f"\n🎯 Fetching transcripts using yt-dlp...")
        print(f"⏱️  Using {args.delay}s delay between requests")

        success_count = 0
        failed_count = 0
        failures = []

        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Fetching transcripts"):
            video_id = row["video_id"]
            title = row.get("title", "Unknown")
            
            result = fetch_transcript_ytdlp(video_id)
            
            df.at[idx, "transcript"] = result.get("transcript")
            df.at[idx, "transcript_available"] = result.get("transcript_available", False)
            
            if result.get("transcript_available"):
                success_count += 1
            else:
                failed_count += 1
                error = result.get("error", "Unknown")
                failures.append((video_id, title, error))
            
            # Delay between requests
            if idx < len(df) - 1:
                time.sleep(args.delay)

        # Save results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False)

        success_rate = (success_count / len(df) * 100) if len(df) > 0 else 0

        print(f"\n✅ Complete!")
        print(f"   ✓ Success: {success_count} videos ({success_rate:.1f}%)")
        print(f"   ✗ Failed:  {failed_count} videos")
        print(f"   Output: {output_path}")

        if failures:
            print(f"\n⚠️  Failed videos (first 10):")
            for video_id, title, error in failures[:10]:
                title_preview = title[:50] + "..." if len(title) > 50 else title
                print(f"     • {video_id}: {title_preview}")
                print(f"       Error: {error}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
