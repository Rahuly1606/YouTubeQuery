"""Quick test script to initialize database tables."""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

async def main():
    print("🔌 Testing database connection...")
    
    try:
        from app.db_connection import init_database, check_database_health, get_table_stats, close_database
        
        # Initialize database and create tables
        await init_database()
        print("✅ Database initialized successfully!")
        print("✅ All tables created!")
        
        # Get table statistics
        print("\n📊 Database Tables:")
        stats = await get_table_stats()
        for table, count in stats.items():
            if isinstance(count, int):
                print(f"   ✓ {table}: {count} records")
            else:
                print(f"   ? {table}: {count}")
        
        # Close connections
        await close_database()
        print("\n🎉 MySQL setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
