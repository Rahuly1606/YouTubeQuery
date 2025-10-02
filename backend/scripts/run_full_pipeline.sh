#!/bin/bash
#
# Complete Data Pipeline for QueryTube
#
# Runs the full data collection, transcript fetching, and indexing pipeline.
#
# Usage:
#   ./scripts/run_full_pipeline.sh
#   ./scripts/run_full_pipeline.sh --channel-id UC_CHANNEL_ID --max-results 50

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║      QueryTube - Full Data Pipeline                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Default values
CHANNEL_ID="${CHANNEL_ID:-UC_x5XG1OV2P6uZZ5FSM9Ttw}"
MAX_RESULTS="${MAX_RESULTS:-100}"
MODEL="${MODEL:-all-MiniLM-L6-v2}"
BATCH_SIZE="${BATCH_SIZE:-32}"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --channel-id)
            CHANNEL_ID="$2"
            shift 2
            ;;
        --max-results)
            MAX_RESULTS="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --batch-size)
            BATCH_SIZE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Channel ID: $CHANNEL_ID"
echo "  Max Results: $MAX_RESULTS"
echo "  Model: $MODEL"
echo "  Batch Size: $BATCH_SIZE"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Please create .env from .env.example and add your YOUTUBE_API_KEY"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    echo "   Please install Python 3.9 or higher"
    exit 1
fi

# Create data directory
mkdir -p data

echo "════════════════════════════════════════════════════════════"
echo " Step 1: Collect YouTube Videos"
echo "════════════════════════════════════════════════════════════"
echo ""

python3 scripts/collect_youtube.py \
    --channel-id "$CHANNEL_ID" \
    --max-results "$MAX_RESULTS" \
    --output data/videos.parquet

if [ $? -ne 0 ]; then
    echo "❌ Video collection failed"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo " Step 2: Fetch Transcripts"
echo "════════════════════════════════════════════════════════════"
echo ""

python3 scripts/get_transcripts.py \
    --input data/videos.parquet \
    --output data/transcripts.parquet \
    --log-failures data/transcript_errors.log

if [ $? -ne 0 ]; then
    echo "❌ Transcript fetching failed"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo " Step 3: Generate Embeddings and Build Index"
echo "════════════════════════════════════════════════════════════"
echo ""

python3 scripts/embed_and_index.py \
    --input data/transcripts.parquet \
    --output-index data/index.faiss \
    --output-embeddings data/embeddings.parquet \
    --model "$MODEL" \
    --batch-size "$BATCH_SIZE" \
    --force

if [ $? -ne 0 ]; then
    echo "❌ Embedding and indexing failed"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Pipeline Complete!                                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Generated files:"
echo "  • data/videos.parquet      - Video metadata"
echo "  • data/transcripts.parquet - Videos with transcripts"
echo "  • data/embeddings.parquet  - Embeddings and metadata"
echo "  • data/index.faiss         - FAISS search index"
echo ""
echo "Next steps:"
echo "  1. Start the backend API:"
echo "     cd backend"
echo "     uvicorn app.main:app --reload"
echo ""
echo "  2. Start the frontend:"
echo "     cd frontend"
echo "     npm run dev"
echo ""
echo "  3. Open http://localhost:3000"
echo ""
