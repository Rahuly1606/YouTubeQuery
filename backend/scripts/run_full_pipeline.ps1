# Complete Data Pipeline for QueryTube (PowerShell version)
#
# Runs the full data collection, transcript fetching, and indexing pipeline.
#
# Usage:
#   .\scripts\run_full_pipeline.ps1
#   .\scripts\run_full_pipeline.ps1 -ChannelId "UC_CHANNEL_ID" -MaxResults 50

param(
    [string]$ChannelId = "UC_x5XG1OV2P6uZZ5FSM9Ttw",
    [int]$MaxResults = 100,
    [string]$Model = "all-MiniLM-L6-v2",
    [int]$BatchSize = 32
)

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      QueryTube - Full Data Pipeline                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuration:"
Write-Host "  Channel ID: $ChannelId"
Write-Host "  Max Results: $MaxResults"
Write-Host "  Model: $Model"
Write-Host "  Batch Size: $BatchSize"
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ Error: .env file not found" -ForegroundColor Red
    Write-Host "   Please create .env from .env.example and add your YOUTUBE_API_KEY"
    exit 1
}

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: python not found" -ForegroundColor Red
    Write-Host "   Please install Python 3.9 or higher"
    exit 1
}

# Create data directory
New-Item -ItemType Directory -Force -Path "data" | Out-Null

Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host " Step 1: Collect YouTube Videos" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

python scripts\collect_youtube.py `
    --channel-id $ChannelId `
    --max-results $MaxResults `
    --output data\videos.parquet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Video collection failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host " Step 2: Fetch Transcripts" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

python scripts\get_transcripts.py `
    --input data\videos.parquet `
    --output data\transcripts.parquet `
    --log-failures data\transcript_errors.log

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Transcript fetching failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host " Step 3: Generate Embeddings and Build Index" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

python scripts\embed_and_index.py `
    --input data\transcripts.parquet `
    --output-index data\index.faiss `
    --output-embeddings data\embeddings.parquet `
    --model $Model `
    --batch-size $BatchSize `
    --force

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Embedding and indexing failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Pipeline Complete!                                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Generated files:"
Write-Host "  • data\videos.parquet      - Video metadata"
Write-Host "  • data\transcripts.parquet - Videos with transcripts"
Write-Host "  • data\embeddings.parquet  - Embeddings and metadata"
Write-Host "  • data\index.faiss         - FAISS search index"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Start the backend API:"
Write-Host "     cd backend"
Write-Host "     uvicorn app.main:app --reload"
Write-Host ""
Write-Host "  2. Start the frontend:"
Write-Host "     cd frontend"
Write-Host "     npm run dev"
Write-Host ""
Write-Host "  3. Open http://localhost:3000"
Write-Host ""
# Full data pipeline script for QueryTube (PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "QueryTube Data Pipeline" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Configuration
$CHANNEL_ID = $env:CHANNEL_ID
$MAX_RESULTS = if ($env:MAX_RESULTS) { $env:MAX_RESULTS } else { 50 }
$YOUTUBE_API_KEY = $env:YOUTUBE_API_KEY

# Check for API key
if (-not $YOUTUBE_API_KEY) {
    Write-Host "Error: YOUTUBE_API_KEY not set" -ForegroundColor Red
    Write-Host "Set it with: `$env:YOUTUBE_API_KEY='your_key'" -ForegroundColor Yellow
    exit 1
}

# Navigate to scripts directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host ""
Write-Host "Step 1: Collecting videos from YouTube..." -ForegroundColor Green
Write-Host "-----------------------------------------"
if (-not $CHANNEL_ID) {
    Write-Host "Warning: CHANNEL_ID not set, skipping collection" -ForegroundColor Yellow
    Write-Host "Set it with: `$env:CHANNEL_ID='your_channel_id'" -ForegroundColor Yellow
}
else {
    python collect_youtube.py `
        --channel-id $CHANNEL_ID `
        --max-results $MAX_RESULTS `
        --api-key $YOUTUBE_API_KEY
    Write-Host "✓ Video collection complete" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Fetching transcripts..." -ForegroundColor Green
Write-Host "-----------------------------------------"
python get_transcripts.py
Write-Host "✓ Transcript fetching complete" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Generating embeddings and building index..." -ForegroundColor Green
Write-Host "-----------------------------------------"
python embed_and_index.py
Write-Host "✓ Embedding generation complete" -ForegroundColor Green

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Pipeline completed successfully!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start backend: cd ..\backend; uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "2. Start frontend: cd ..\frontend; npm run dev" -ForegroundColor White
Write-Host "3. Visit: http://localhost:3000" -ForegroundColor White
