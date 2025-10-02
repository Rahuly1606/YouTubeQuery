#!/usr/bin/env python3
"""
Embedding and Indexing Script

Generates vector embeddings using Sentence-Transformers and builds FAISS index
for semantic search.

Usage:
    python embed_and_index.py
    python embed_and_index.py --model all-mpnet-base-v2 --batch-size 64
    python embed_and_index.py --input data/transcripts.parquet --output-index data/index.faiss
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


def load_transcripts(input_path: Path) -> pd.DataFrame:
    """Load transcripts from parquet file."""
    if not input_path.exists():
        raise FileNotFoundError(
            f"Transcripts file not found: {input_path}\n"
            "Please run get_transcripts.py first."
        )

    df = pd.read_parquet(input_path)

    # Filter videos with transcripts
    df = df[df["transcript"].notna() & (df["transcript"] != "")]

    return df


def generate_embeddings(
    texts: list[str],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32,
) -> np.ndarray:
    """Generate embeddings using Sentence-Transformers."""
    print(f"\n🤖 Loading model: {model_name}")

    # Check if HuggingFace token is needed
    hf_token = os.getenv("HF_TOKEN")
    if hf_token and hf_token != "your_huggingface_token_here":
        os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token

    model = SentenceTransformer(model_name)
    embedding_dim = model.get_sentence_embedding_dimension()

    print(f"✓ Model loaded (dimension: {embedding_dim})")
    print(f"\n🔢 Generating embeddings for {len(texts)} texts...")

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,  # Normalize for cosine similarity
    )

    print(f"✓ Generated embeddings: shape {embeddings.shape}")

    return embeddings


def build_faiss_index(
    embeddings: np.ndarray,
    metric: str = "cosine",
) -> faiss.Index:
    """Build FAISS index for vector search."""
    print(f"\n🔨 Building FAISS index...")
    print(f"   Metric: {metric}")
    print(f"   Vectors: {embeddings.shape[0]}")
    print(f"   Dimensions: {embeddings.shape[1]}")

    dimension = embeddings.shape[1]

    # Use IndexFlatIP (inner product) for cosine similarity
    # Embeddings are already normalized, so IP = cosine similarity
    if metric == "cosine":
        index = faiss.IndexFlatIP(dimension)
    elif metric == "euclidean":
        index = faiss.IndexFlatL2(dimension)
    else:
        raise ValueError(f"Unsupported metric: {metric}. Use 'cosine' or 'euclidean'")

    # Add vectors to index
    index.add(embeddings.astype(np.float32))

    print(f"✓ Index built with {index.ntotal} vectors")

    return index


def save_index(index: faiss.Index, output_path: Path):
    """Save FAISS index to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_path))
    print(f"✓ Index saved to: {output_path}")


def save_embeddings(df: pd.DataFrame, embeddings: np.ndarray, output_path: Path):
    """Save embeddings and metadata to parquet."""
    # Add embeddings to DataFrame
    df = df.copy()
    df["embedding"] = list(embeddings)

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    print(f"✓ Embeddings and metadata saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate embeddings and build FAISS index for semantic search"
    )

    parser.add_argument(
        "--input",
        default="data/transcripts.parquet",
        help="Input parquet file with transcripts (default: data/transcripts.parquet)",
    )
    parser.add_argument(
        "--output-index",
        default="data/index.faiss",
        help="Output FAISS index file (default: data/index.faiss)",
    )
    parser.add_argument(
        "--output-embeddings",
        default="data/embeddings.parquet",
        help="Output embeddings parquet file (default: data/embeddings.parquet)",
    )
    parser.add_argument(
        "--model",
        default="all-MiniLM-L6-v2",
        help="Sentence-Transformer model name (default: all-MiniLM-L6-v2)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for embedding generation (default: 32)",
    )
    parser.add_argument(
        "--metric",
        default="cosine",
        choices=["cosine", "euclidean"],
        help="Distance metric for FAISS index (default: cosine)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing index",
    )

    args = parser.parse_args()

    try:
        # Check if output exists
        output_index = Path(args.output_index)
        if output_index.exists() and not args.force:
            print(f"⚠️  Index already exists: {output_index}")
            print("   Use --force to overwrite")
            sys.exit(0)

        # Load transcripts
        print(f"📂 Loading transcripts from: {args.input}")
        df = load_transcripts(Path(args.input))
        print(f"✓ Loaded {len(df)} videos with transcripts")

        if len(df) == 0:
            print("❌ No videos with transcripts found!")
            print("   Please run get_transcripts.py to fetch transcripts first.")
            sys.exit(1)

        # Show statistics
        print(f"\n📊 Dataset statistics:")
        print(f"   Total videos: {len(df)}")
        print(f"   Avg transcript length: {df['transcript'].str.len().mean():.0f} chars")
        print(f"   Date range: {df['published_at'].min()} to {df['published_at'].max()}")

        # Generate embeddings
        texts = df["transcript"].tolist()
        embeddings = generate_embeddings(
            texts,
            model_name=args.model,
            batch_size=args.batch_size,
        )

        # Build FAISS index
        index = build_faiss_index(embeddings, metric=args.metric)

        # Save index
        print(f"\n💾 Saving outputs...")
        save_index(index, output_index)

        # Save embeddings and metadata
        save_embeddings(df, embeddings, Path(args.output_embeddings))

        # Summary
        print(f"\n✅ Success!")
        print(f"   Model: {args.model}")
        print(f"   Vectors indexed: {index.ntotal}")
        print(f"   Dimension: {embeddings.shape[1]}")
        print(f"   Metric: {args.metric}")
        print(f"\n   Index: {output_index}")
        print(f"   Embeddings: {args.output_embeddings}")

        print(f"\n🚀 Ready for semantic search!")
        print(f"   Start the backend API:")
        print(f"     cd backend")
        print(f"     uvicorn app.main:app --reload")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
