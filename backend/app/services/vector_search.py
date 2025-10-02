"""
Vector Search Service

Handles embedding generation, FAISS indexing, and similarity search.
"""

import os
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from loguru import logger

from app.config import settings


class VectorSearchService:
    """Service for vector embeddings and semantic search."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        index_path: Optional[str] = None,
        embeddings_path: Optional[str] = None,
    ):
        """
        Initialize vector search service.

        Args:
            model_name: Sentence-Transformer model name
            index_path: Path to save/load FAISS index
            embeddings_path: Path to save/load embeddings parquet
        """
        self.model_name = model_name
        self.index_path = index_path or settings.index_path
        self.embeddings_path = embeddings_path or settings.embeddings_path

        # Initialize model
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        # FAISS index and metadata
        self.index: Optional[faiss.Index] = None
        self.metadata: Optional[pd.DataFrame] = None

    def load_index(self):
        """Load existing FAISS index and metadata from disk."""
        try:
            # Load FAISS index
            if not os.path.exists(self.index_path):
                raise FileNotFoundError(f"Index not found: {self.index_path}")

            logger.info(f"Loading FAISS index from {self.index_path}")
            self.index = faiss.read_index(self.index_path)

            # Load metadata
            if not os.path.exists(self.embeddings_path):
                raise FileNotFoundError(f"Embeddings metadata not found: {self.embeddings_path}")

            logger.info(f"Loading metadata from {self.embeddings_path}")
            self.metadata = pd.read_parquet(self.embeddings_path)

            logger.info(
                f"✓ Loaded index with {self.index.ntotal} vectors, "
                f"{len(self.metadata)} metadata entries"
            )

        except Exception as e:
            logger.error(f"Error loading index: {e}")
            raise

    def build_index(
        self,
        model_name: Optional[str] = None,
        batch_size: Optional[int] = None,
        force_rebuild: bool = False,
    ) -> tuple[int, int]:
        """
        Build FAISS index from transcript data.

        Args:
            model_name: Override embedding model
            batch_size: Batch size for embedding generation
            force_rebuild: Rebuild even if index exists

        Returns:
            Tuple of (videos_indexed, index_size)
        """
        try:
            # Check if index exists
            if os.path.exists(self.index_path) and not force_rebuild:
                logger.warning("Index already exists. Use force_rebuild=True to rebuild.")
                self.load_index()
                return len(self.metadata), self.index.ntotal

            # Load model if different
            if model_name and model_name != self.model_name:
                logger.info(f"Loading new model: {model_name}")
                self.model = SentenceTransformer(model_name)
                self.model_name = model_name
                self.embedding_dim = self.model.get_sentence_embedding_dimension()

            # Load transcript data
            transcripts_path = settings.transcripts_path
            if not os.path.exists(transcripts_path):
                raise FileNotFoundError(
                    f"Transcripts not found: {transcripts_path}. "
                    "Please run data collection pipeline first."
                )

            logger.info(f"Loading transcripts from {transcripts_path}")
            df = pd.read_parquet(transcripts_path)

            # Filter videos with transcripts
            df = df[df["transcript"].notna() & (df["transcript"] != "")]
            logger.info(f"Found {len(df)} videos with transcripts")

            if len(df) == 0:
                raise ValueError("No videos with transcripts found")

            # Generate embeddings
            logger.info("Generating embeddings...")
            batch_size = batch_size or settings.embedding_batch_size
            texts = df["transcript"].tolist()

            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
            )

            # Create FAISS index
            logger.info("Building FAISS index...")
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine after normalization)

            # Normalize vectors for cosine similarity
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings.astype(np.float32))

            # Save index
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            logger.info(f"Saving index to {self.index_path}")
            faiss.write_index(self.index, self.index_path)

            # Save metadata with embeddings
            df["embedding"] = list(embeddings)
            logger.info(f"Saving metadata to {self.embeddings_path}")
            df.to_parquet(self.embeddings_path, index=False)

            self.metadata = df

            logger.info(f"✓ Index built successfully: {len(df)} vectors")
            return len(df), self.index.ntotal

        except Exception as e:
            logger.error(f"Error building index: {e}")
            raise

    def search(
        self,
        query: str,
        top_k: int = 5,
        metric: str = "cosine",
        min_score: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar videos using semantic search.

        Args:
            query: Search query text
            top_k: Number of results to return
            metric: Distance metric (cosine, euclidean, dot_product)
            min_score: Minimum similarity score threshold

        Returns:
            List of search results with scores and metadata
        """
        if self.index is None or self.metadata is None:
            raise ValueError("Index not loaded. Call load_index() first.")

        try:
            # Generate query embedding
            query_embedding = self.model.encode(
                [query],
                convert_to_numpy=True,
            )

            # Normalize for cosine similarity
            faiss.normalize_L2(query_embedding)

            # Search
            distances, indices = self.index.search(
                query_embedding.astype(np.float32),
                top_k,
            )

            # Build results
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1:  # FAISS returns -1 for unfilled results
                    continue

                # Convert distance to score (0-1 range)
                # For normalized vectors with inner product, distance is already cosine similarity
                score = float(dist)

                # Apply minimum score filter
                if min_score is not None and score < min_score:
                    continue

                # Get metadata
                row = self.metadata.iloc[idx]

                # Extract snippet (first 200 chars of transcript)
                snippet = row.get("transcript", "")[:200] + "..." if row.get("transcript") else None

                result = {
                    "video_id": row["video_id"],
                    "title": row["title"],
                    "channel": row.get("channel", "Unknown"),
                    "channel_id": row.get("channel_id", ""),
                    "published_at": row.get("published_at", ""),
                    "thumbnail_url": row.get("thumbnail_url", ""),
                    "description": row.get("description"),
                    "score": score,
                    "snippet": snippet,
                    "start_time": 0.0,  # TODO: Find actual snippet location
                    "view_count": row.get("view_count"),
                    "duration": row.get("duration"),
                }

                results.append(result)

            logger.info(f"Found {len(results)} results for query: '{query[:50]}'")
            return results

        except Exception as e:
            logger.error(f"Search error: {e}")
            raise

    def get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        return self.model.encode([text], convert_to_numpy=True)[0]

    def batch_embed(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
