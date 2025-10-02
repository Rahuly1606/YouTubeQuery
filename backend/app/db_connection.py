"""
Database connection and session management.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from .config import settings
from .database import Base

logger = logging.getLogger(__name__)

# Create async engine
engine = None
AsyncSessionLocal = None


async def init_database():
    """Initialize database connection and create tables."""
    global engine, AsyncSessionLocal
    
    try:
        # Get database URL
        database_url = settings.get_database_url()
        logger.info(f"Connecting to database: {database_url.split('@')[0]}@...")
        
        # Create async engine
        engine = create_async_engine(
            database_url,
            echo=settings.debug,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_pre_ping=True,  # Validate connections before use
        )
        
        # Create session factory
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_database():
    """Close database connections."""
    global engine
    
    if engine:
        await engine.dispose()
        logger.info("Database connections closed")


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session with automatic cleanup."""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions."""
    async with get_db_session() as session:
        yield session


# Health check function
async def check_database_health() -> dict:
    """Check database connectivity and return status."""
    try:
        async with get_db_session() as session:
            # Simple query to test connection
            await session.execute("SELECT 1")
            return {
                "status": "healthy",
                "database": "connected",
                "url": settings.get_database_url().split('@')[0] + "@..."
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# Migration helper functions
async def reset_database():
    """Drop and recreate all tables. USE WITH CAUTION!"""
    if not engine:
        raise RuntimeError("Database not initialized")
    
    logger.warning("Resetting database - all data will be lost!")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database reset completed")


async def get_table_stats() -> dict:
    """Get statistics about database tables."""
    stats = {}
    
    try:
        async with get_db_session() as session:
            # Count records in each table
            from .database import Video, Transcript, Embedding, SearchLog
            
            tables = [
                ("videos", Video),
                ("transcripts", Transcript), 
                ("embeddings", Embedding),
                ("search_logs", SearchLog),
            ]
            
            for table_name, model in tables:
                try:
                    count = await session.scalar(
                        f"SELECT COUNT(*) FROM {table_name}"
                    )
                    stats[table_name] = count or 0
                except Exception as e:
                    stats[table_name] = f"Error: {e}"
            
    except Exception as e:
        stats["error"] = str(e)
    
    return stats