#!/usr/bin/env python3
"""
MySQL Database Setup Script for QueryTube

This script helps you set up MySQL for QueryTube and test the connection.
"""

import sys
import os
import asyncio
import subprocess
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

try:
    from app.config import settings
    from app.db_connection import init_database, check_database_health, get_table_stats
    from app.database import Base
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you're running this from the backend directory")
    sys.exit(1)


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_error(text):
    """Print error message."""
    print(f"❌ {text}")


def print_warning(text):
    """Print warning message."""
    print(f"⚠️  {text}")


def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")


def check_mysql_installed():
    """Check if MySQL is installed."""
    try:
        result = subprocess.run(
            ["mysql", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"MySQL found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print_error("MySQL not found in PATH")
    return False


def check_mysql_service():
    """Check if MySQL service is running."""
    try:
        # Try to connect to MySQL
        result = subprocess.run(
            ["mysql", "-u", "root", "-e", "SELECT 1;"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("MySQL service is running")
            return True
    except Exception:
        pass
    
    print_warning("MySQL service may not be running")
    return False


def create_database():
    """Create the QueryTube database."""
    db_name = settings.db_name
    db_user = settings.db_user
    db_password = settings.db_password
    
    try:
        # Create database
        cmd = [
            "mysql",
            "-u", db_user,
            "-e", f"CREATE DATABASE IF NOT EXISTS {db_name};"
        ]
        
        if db_password:
            cmd.insert(-2, f"-p{db_password}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"Database '{db_name}' created successfully")
            return True
        else:
            print_error(f"Failed to create database: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Error creating database: {e}")
        return False


async def test_connection():
    """Test the database connection."""
    try:
        await init_database()
        health = await check_database_health()
        
        if health["status"] == "healthy":
            print_success("Database connection successful!")
            print_info(f"Connected to: {health['url']}")
            return True
        else:
            print_error(f"Database connection failed: {health.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False


async def show_tables():
    """Show table statistics."""
    try:
        stats = await get_table_stats()
        
        print_info("Database table statistics:")
        for table, count in stats.items():
            if isinstance(count, int):
                print(f"  📊 {table}: {count} records")
            else:
                print(f"  ❗ {table}: {count}")
                
    except Exception as e:
        print_error(f"Failed to get table stats: {e}")


def print_mysql_setup_guide():
    """Print MySQL installation and setup guide."""
    print_header("MySQL Setup Guide")
    
    print("🔧 Installation Options:")
    print()
    print("1. Windows:")
    print("   - Download MySQL Community Server from: https://dev.mysql.com/downloads/mysql/")
    print("   - Or use Chocolatey: choco install mysql")
    print("   - Or use XAMPP: https://www.apachefriends.org/")
    print()
    print("2. macOS:")
    print("   - Homebrew: brew install mysql")
    print("   - MySQL Community Server: https://dev.mysql.com/downloads/mysql/")
    print()
    print("3. Linux:")
    print("   - Ubuntu/Debian: sudo apt install mysql-server")
    print("   - CentOS/RHEL: sudo yum install mysql-server")
    print()
    print("4. Docker (Recommended for development):")
    print("   docker run --name querytube-mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0")
    print()
    print("📝 After installation:")
    print("1. Start MySQL service")
    print("2. Set root password (if not set)")
    print("3. Create database user (optional)")
    print("4. Update .env file with connection details")


def print_env_config():
    """Print environment configuration guide."""
    print_header("Environment Configuration")
    
    print("📝 Update your backend/.env file:")
    print()
    print("# MySQL Configuration")
    print("DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/querytube")
    print("DB_HOST=localhost")
    print("DB_PORT=3306")
    print("DB_NAME=querytube")
    print("DB_USER=root")
    print("DB_PASSWORD=your_password_here")
    print()
    print("🔐 Security Tips:")
    print("- Use a strong password")
    print("- Create a dedicated database user (not root)")
    print("- Limit user permissions to the querytube database only")
    print()
    print("🏗️ Production Setup:")
    print("- Use environment variables for sensitive data")
    print("- Enable SSL/TLS connections")
    print("- Configure connection pooling")
    print("- Set up database backups")


async def main():
    """Main setup function."""
    print_header("QueryTube MySQL Database Setup")
    
    print("🔍 Checking current configuration...")
    print(f"Database URL: {settings.get_database_url()}")
    print(f"Host: {settings.db_host}:{settings.db_port}")
    print(f"Database: {settings.db_name}")
    print(f"User: {settings.db_user}")
    
    # Check if using MySQL
    if not settings.get_database_url().startswith("mysql"):
        print_warning("Not configured for MySQL. Update DATABASE_URL in .env file.")
        print_env_config()
        return
    
    # Check MySQL installation
    mysql_installed = check_mysql_installed()
    if not mysql_installed:
        print_mysql_setup_guide()
        return
    
    # Check MySQL service
    service_running = check_mysql_service()
    if not service_running:
        print_warning("Start MySQL service and try again")
        return
    
    # Create database
    print("\n🏗️ Creating database...")
    db_created = create_database()
    
    # Test connection
    print("\n🔌 Testing database connection...")
    connection_ok = await test_connection()
    
    if connection_ok:
        print("\n📊 Database tables created successfully!")
        await show_tables()
        
        print_header("Setup Complete!")
        print_success("MySQL database is ready for QueryTube!")
        print()
        print("🚀 Next steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Start the backend: uvicorn app.main:app --reload")
        print("3. Run data collection: python scripts/collect_youtube.py")
        
    else:
        print_header("Setup Failed")
        print("❌ Database setup incomplete. Check the errors above.")
        print()
        print("🔧 Troubleshooting:")
        print("1. Verify MySQL is running")
        print("2. Check credentials in .env file") 
        print("3. Ensure database user has proper permissions")
        print("4. Test manual connection: mysql -u root -p")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)