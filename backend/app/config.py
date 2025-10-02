"""
QueryTube Backend Configuration

Centralized configuration management using Pydantic Settings.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==================== API Configuration ====================
    app_name: str = "QueryTube API"
    app_version: str = "1.0.0"
    debug: bool = False
    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")

    # ==================== CORS ====================
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        alias="CORS_ORIGINS",
    )

    # ==================== YouTube API ====================
    youtube_api_key: str = Field(..., alias="YOUTUBE_API_KEY")
    youtube_api_quota_limit: int = Field(default=10000, alias="YOUTUBE_API_QUOTA_LIMIT")
    default_channel_id: Optional[str] = Field(
        default="UC_x5XG1OV2P6uZZ5FSM9Ttw",
        alias="DEFAULT_CHANNEL_ID",
    )
    max_results_per_request: int = Field(default=50, alias="MAX_RESULTS_PER_REQUEST")

    # ==================== HuggingFace ====================
    hf_token: Optional[str] = Field(default=None, alias="HF_TOKEN")

    # ==================== Vector Store ====================
    vector_store: str = Field(default="faiss", alias="VECTOR_STORE")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    embedding_batch_size: int = Field(default=32, alias="EMBEDDING_BATCH_SIZE")
    distance_metric: str = Field(default="cosine", alias="DISTANCE_METRIC")

    # ==================== Pinecone (Optional) ====================
    pinecone_api_key: Optional[str] = Field(default=None, alias="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(
        default=None, alias="PINECONE_ENVIRONMENT"
    )
    pinecone_index_name: str = Field(default="querytube", alias="PINECONE_INDEX_NAME")

    # ==================== Database ====================
    database_url: str = Field(
        default="sqlite:///./querytube.db", alias="DATABASE_URL"
    )
    
    # MySQL Configuration
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=3306, alias="DB_PORT")
    db_name: str = Field(default="querytube", alias="DB_NAME")
    db_user: str = Field(default="root", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")
    
    # Database Pool Settings
    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, alias="DB_MAX_OVERFLOW")
    db_pool_timeout: int = Field(default=30, alias="DB_POOL_TIMEOUT")

    # ==================== Data Paths ====================
    data_dir: str = Field(default="./data", alias="DATA_DIR")
    index_path: str = Field(default="./data/index.faiss", alias="INDEX_PATH")
    embeddings_path: str = Field(
        default="./data/embeddings.parquet", alias="EMBEDDINGS_PATH"
    )
    videos_path: str = Field(default="./data/videos.parquet", alias="VIDEOS_PATH")
    transcripts_path: str = Field(
        default="./data/transcripts.parquet", alias="TRANSCRIPTS_PATH"
    )

    # ==================== Search Configuration ====================
    default_top_k: int = Field(default=5, alias="DEFAULT_TOP_K")
    max_top_k: int = Field(default=50, alias="MAX_TOP_K")
    min_similarity_score: float = Field(default=0.3, alias="MIN_SIMILARITY_SCORE")

    # ==================== Rate Limiting ====================
    rate_limit_per_minute: int = Field(default=60, alias="RATE_LIMIT_PER_MINUTE")

    # ==================== Logging ====================
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins

    def get_faiss_index_path(self) -> str:
        """Get the full path to FAISS index."""
        return self.index_path

    def get_embeddings_path(self) -> str:
        """Get the full path to embeddings file."""
        return self.embeddings_path

    def validate_youtube_api_key(self) -> bool:
        """Check if YouTube API key is configured."""
        return bool(self.youtube_api_key and self.youtube_api_key != "your_youtube_api_key_here")

    def get_mysql_url(self) -> str:
        """Construct MySQL database URL from components."""
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def get_database_url(self) -> str:
        """Get the appropriate database URL based on configuration."""
        if self.database_url.startswith("mysql"):
            return self.database_url
        elif "mysql" in self.database_url.lower() or self.db_host != "localhost":
            return self.get_mysql_url()
        return self.database_url


# Create global settings instance
settings = Settings()
