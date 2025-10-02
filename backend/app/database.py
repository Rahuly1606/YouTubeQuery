"""
SQLAlchemy database models for QueryTube.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import json

Base = declarative_base()


class Video(Base):
    """Video metadata table."""
    
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    channel_id = Column(String(50), nullable=False, index=True)
    channel_title = Column(String(200), nullable=False)
    published_at = Column(DateTime, nullable=False)
    duration = Column(String(20))  # ISO 8601 format
    view_count = Column(String(20))  # Store as string to handle large numbers
    like_count = Column(String(20))
    comment_count = Column(String(20))
    thumbnail_url = Column(String(500))
    language = Column(String(10))
    category_id = Column(String(10))
    tags = Column(Text)  # JSON string
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_video_channel', 'channel_id'),
        Index('idx_video_published', 'published_at'),
        Index('idx_video_title', 'title'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'video_id': self.video_id,
            'title': self.title,
            'description': self.description,
            'channel_id': self.channel_id,
            'channel_title': self.channel_title,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'duration': self.duration,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'thumbnail_url': self.thumbnail_url,
            'language': self.language,
            'category_id': self.category_id,
            'tags': json.loads(self.tags) if self.tags else [],
        }


class Transcript(Base):
    """Video transcript table."""
    
    __tablename__ = "transcripts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(20), nullable=False, index=True)
    language = Column(String(10), nullable=False)
    text = Column(Text, nullable=False)
    start_time = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    
    # Full transcript text for search
    full_transcript = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_transcript_video', 'video_id'),
        Index('idx_transcript_time', 'video_id', 'start_time'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'video_id': self.video_id,
            'language': self.language,
            'text': self.text,
            'start_time': self.start_time,
            'duration': self.duration,
            'full_transcript': self.full_transcript,
        }


class Embedding(Base):
    """Video embedding table."""
    
    __tablename__ = "embeddings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(20), nullable=False, index=True)
    model_name = Column(String(100), nullable=False)
    embedding_vector = Column(Text, nullable=False)  # JSON string of the vector
    text_content = Column(Text, nullable=False)  # The text that was embedded
    
    # Embedding metadata
    vector_dimension = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_embedding_video', 'video_id'),
        Index('idx_embedding_model', 'model_name'),
    )
    
    def get_vector(self):
        """Get embedding vector as list."""
        return json.loads(self.embedding_vector)
    
    def set_vector(self, vector):
        """Set embedding vector from list."""
        self.embedding_vector = json.dumps(vector)
        self.vector_dimension = len(vector)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'video_id': self.video_id,
            'model_name': self.model_name,
            'vector': self.get_vector(),
            'text_content': self.text_content,
            'vector_dimension': self.vector_dimension,
        }


class SearchLog(Base):
    """Search query logs."""
    
    __tablename__ = "search_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(500), nullable=False)
    results_count = Column(Integer, nullable=False)
    processing_time = Column(Float, nullable=False)
    user_ip = Column(String(45))  # IPv6 compatible
    user_agent = Column(String(500))
    
    # Search parameters
    top_k = Column(Integer, nullable=False)
    metric = Column(String(20), nullable=False)
    min_score = Column(Float)
    
    # Timestamp
    created_at = Column(DateTime, server_default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_search_query', 'query'),
        Index('idx_search_time', 'created_at'),
    )


class SystemStatus(Base):
    """System status and health metrics."""
    
    __tablename__ = "system_status"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(String(500), nullable=False)
    description = Column(String(500))
    
    # Timestamp
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_status_metric', 'metric_name'),
    )