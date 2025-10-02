#!/usr/bin/env python3
"""
QueryTube - Test Script

Quick verification that all components are working correctly.
Run this after setting up the project to verify everything is configured properly.
"""

import os
import sys
from pathlib import Path
import subprocess

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

def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Requires Python 3.9+")
        return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    print_header("Checking Environment Configuration")
    
    env_path = Path(".env")
    if not env_path.exists():
        print_error(".env file not found")
        print("   Run: cp .env.example .env")
        return False
    
    print_success(".env file exists")
    
    # Check for YouTube API key
    with open(env_path, 'r') as f:
        content = f.read()
        if 'YOUTUBE_API_KEY=' in content and 'your_youtube_api_key_here' not in content:
            print_success("YouTube API key configured")
            return True
        else:
            print_error("YouTube API key not configured in .env")
            print("   Add your YouTube API key to .env file")
            return False

def check_backend_dependencies():
    """Check if backend dependencies are installed."""
    print_header("Checking Backend Dependencies")
    
    try:
        import fastapi
        print_success(f"fastapi {fastapi.__version__}")
    except ImportError:
        print_error("fastapi not installed")
        print("   Run: cd backend && pip install -r requirements.txt")
        return False
    
    try:
        import sentence_transformers
        print_success("sentence-transformers installed")
    except ImportError:
        print_error("sentence-transformers not installed")
        return False
    
    try:
        import faiss
        print_success("faiss installed")
    except ImportError:
        print_error("faiss not installed")
        return False
    
    return True

def check_data_files():
    """Check if data files exist."""
    print_header("Checking Data Files")
    
    data_dir = Path("data")
    if not data_dir.exists():
        print_warning("data/ directory doesn't exist yet")
        print("   Run the data pipeline to create it")
        return False
    
    files_to_check = {
        "videos.parquet": "Video metadata",
        "transcripts.parquet": "Video transcripts",
        "embeddings.parquet": "Embeddings metadata",
        "index.faiss": "FAISS search index",
    }
    
    all_exist = True
    for filename, description in files_to_check.items():
        filepath = data_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print_success(f"{description}: {filename} ({size_mb:.1f} MB)")
        else:
            print_warning(f"{description}: {filename} not found")
            all_exist = False
    
    if not all_exist:
        print("\n   Run data pipeline:")
        print("   PowerShell: .\\scripts\\run_full_pipeline.ps1")
        print("   Bash: ./scripts/run_full_pipeline.sh")
    
    return all_exist

def check_backend_port():
    """Check if backend port is available."""
    print_header("Checking Port Availability")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print_warning("Port 8000 is already in use")
            print("   Backend might already be running")
            print("   Or another service is using the port")
            return False
        else:
            print_success("Port 8000 is available")
            return True
    except Exception as e:
        print_error(f"Error checking port: {e}")
        return False

def check_node():
    """Check if Node.js is installed."""
    print_header("Checking Node.js Installation")
    
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Node.js {version}")
            
            # Check npm
            npm_result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True
            )
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print_success(f"npm {npm_version}")
                return True
        return False
    except FileNotFoundError:
        print_error("Node.js not found")
        print("   Download from: https://nodejs.org/")
        return False

def main():
    """Run all checks."""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + "  QueryTube - System Check".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Backend Dependencies", check_backend_dependencies),
        ("Node.js", check_node),
        ("Data Files", check_data_files),
        ("Port Availability", check_backend_port),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Error in {name}: {e}")
            results[name] = False
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Passed: {passed}/{total} checks")
    
    if passed == total:
        print("\n" + "="*60)
        print("🎉 All checks passed! You're ready to run QueryTube!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Start backend:  cd backend && uvicorn app.main:app --reload")
        print("  2. Start frontend: cd frontend && npm run dev")
        print("  3. Open browser:   http://localhost:3000")
    elif passed >= total - 2:
        print("\n" + "="*60)
        print("⚠️  Almost there! Fix the warnings above and you're ready!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ Some issues need to be fixed. See errors above.")
        print("="*60)
        print("\nQuick fixes:")
        print("  • Install dependencies: cd backend && pip install -r requirements.txt")
        print("  • Create .env file: cp .env.example .env")
        print("  • Add YouTube API key to .env")
        print("  • Run data pipeline: scripts/run_full_pipeline.ps1")
    
    print("\n📚 For help, see:")
    print("  • QUICKSTART.md - 5-minute setup guide")
    print("  • MANUAL_STEPS.md - API key setup")
    print("  • README.md - Full documentation\n")

if __name__ == "__main__":
    main()
