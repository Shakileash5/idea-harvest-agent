#!/usr/bin/env python3
"""
Setup script for Idea Harvest Agent
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""# Reddit API credentials
REDDIT_CLIENT_ID=2XAU4xsPicbSlOwt9RSk-Q
REDDIT_CLIENT_SECRET=LUgsC_uowCDGJIeJoLDtUfby3Q8p-A
REDDIT_USER_AGENT=idea-harvest-agent/1.0

# Google AI API key
GOOGLE_AI_API_KEY=your_google_ai_api_key

# Optional: SerpAPI for enhanced search
SERPAPI_KEY=your_serpapi_key
""")
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your API keys")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    directories = ["templates", "scrapers", "data", "output"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def test_imports():
    """Test if all imports work"""
    print("🧪 Testing imports...")
    try:
        import praw
        import requests
        import google.generativeai
        import pandas
        import numpy
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)

def main():
    """Main setup function"""
    print("🚀 Setting up Idea Harvest Agent...")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    create_directories()
    create_env_file()
    test_imports()
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python main.py")
    print("3. Or run: python web_interface.py")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
