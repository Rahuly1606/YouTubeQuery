"""Quick status check for YouTube Query project"""
import sys
from pathlib import Path

def check_status():
    print("=" * 60)
    print("📊 YOUTUBE QUERY - PROJECT STATUS")
    print("=" * 60)
    
    data_dir = Path("data")
    
    # Check videos
    videos_path = data_dir / "videos.parquet"
    if videos_path.exists():
        import pandas as pd
        df = pd.read_parquet(videos_path)
        
        # Check if demo data
        is_demo = df['video_id'].astype(str).str.startswith('demo').any()
        
        print(f"\n✅ Videos: {len(df)} {'(DEMO DATA)' if is_demo else '(REAL DATA)'}")
        if len(df) > 0:
            print(f"   Channel: {df.iloc[0]['channel']}")
            print(f"   Sample: {df.iloc[0]['title'][:50]}...")
    else:
        print(f"\n❌ No videos found!")
        print(f"   Run: python scripts/collect_youtube.py --channel-id CHANNEL_ID --max-results 30")
        return False
    
    # Check transcripts
    transcripts_path = data_dir / "transcripts.parquet"
    if transcripts_path.exists():
        df_trans = pd.read_parquet(transcripts_path)
        if 'transcript' in df_trans.columns:
            has_trans = len(df_trans[df_trans['transcript'].notna()])
            success_rate = has_trans / len(df_trans) * 100 if len(df_trans) > 0 else 0
            
            if has_trans > 0:
                print(f"\n✅ Transcripts: {has_trans}/{len(df_trans)} ({success_rate:.1f}% success)")
            else:
                print(f"\n⚠️  Transcripts: 0/{len(df_trans)} (0% success)")
                print(f"   Run: python scripts/get_transcripts.py --delay 2.5 --max-retries 5")
                return False
        else:
            print(f"\n⚠️  Transcript column missing")
            return False
    else:
        print(f"\n❌ No transcripts found!")
        print(f"   Run: python scripts/get_transcripts.py --delay 2.5 --max-retries 5")
        return False
    
    # Check index
    index_path = data_dir / "index.faiss"
    if index_path.exists():
        print(f"\n✅ Search index: Ready")
    else:
        print(f"\n⚠️  Search index: Not found")
        print(f"   Run: python scripts/embed_and_index.py")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL SYSTEMS READY!")
    print("=" * 60)
    print("\n🚀 Start the application:")
    print("   Terminal 1: uvicorn app.main:app --reload")
    print("   Terminal 2: cd ../frontend && npm run dev")
    print("   Browser: http://localhost:3000")
    
    return True

if __name__ == "__main__":
    success = check_status()
    sys.exit(0 if success else 1)
