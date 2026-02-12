#!/usr/bin/env python3
"""
Setup and validation script for the chunk-and-transcribe project
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    # Try standard path first
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
            return True
    except FileNotFoundError:
        pass

    # Try Homebrew ARM64 path (Apple Silicon)
    try:
        result = subprocess.run(['/opt/homebrew/bin/ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed (found at /opt/homebrew/bin/ffmpeg)")
            print("   ℹ️  Add to PATH: export PATH=\"/opt/homebrew/bin:$PATH\"")
            return True
    except FileNotFoundError:
        pass

    # Try Homebrew Intel path
    try:
        result = subprocess.run(['/usr/local/bin/ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed (found at /usr/local/bin/ffmpeg)")
            print("   ℹ️  Add to PATH: export PATH=\"/usr/local/bin:$PATH\"")
            return True
    except FileNotFoundError:
        pass

    print("❌ FFmpeg not found in system PATH")
    print("   Install FFmpeg:")
    print("   macOS: brew install ffmpeg")
    print("   Linux: sudo apt-get install ffmpeg")
    print("   Windows: Download from https://ffmpeg.org/download.html")
    print()
    print("   Or add to ~/.zshrc or ~/.bash_profile:")
    print("   export PATH=\"/opt/homebrew/bin:$PATH\"  # For Apple Silicon")
    print("   export PATH=\"/usr/local/bin:$PATH\"     # For Intel Mac")
    return False

def check_required_packages():
    """Check if required Python packages are installed"""
    required = ['requests', 'pydub', 'dotenv']
    missing = []

    for package in required:
        try:
            __import__(package if package != 'dotenv' else 'dotenv')
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            missing.append(package)

    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and is configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Create .env file with:")
        print("   HF_TOKEN=your_token")
        print("   HF_INFERENCE_ENDPOINT=your_endpoint_url")
        return False

    try:
        from dotenv import load_dotenv
        load_dotenv()

        hf_token = os.getenv('HF_TOKEN')
        hf_endpoint = os.getenv('HF_INFERENCE_ENDPOINT')

        if not hf_token:
            print("❌ HF_TOKEN not set in .env")
            return False

        if not hf_endpoint:
            print("❌ HF_INFERENCE_ENDPOINT not set in .env")
            return False

        print("✅ .env file is configured")
        return True
    except Exception as e:
        print(f"❌ Error reading .env: {str(e)}")
        return False

def check_folders():
    """Check if required folders exist"""
    folders = ['audio', 'chunks']

    for folder in folders:
        if os.path.exists(folder):
            print(f"✅ {folder}/ folder exists")
        else:
            print(f"⚠️  {folder}/ folder not found (will be created if needed)")

    # Create audio folder if it doesn't exist
    if not os.path.exists('audio'):
        os.makedirs('audio')
        print("   Created audio/ folder")

    return True

def check_audio_files():
    """Check if there are FLAC files in audio folder"""
    if not os.path.exists('audio'):
        print("❌ audio/ folder not found")
        return False

    flac_files = [f for f in os.listdir('audio') if f.lower().endswith('.flac')]

    if not flac_files:
        print("⚠️  No FLAC files in audio/ folder")
        print("   Add .flac files to the audio/ folder before running the script")
        return False

    print(f"✅ Found {len(flac_files)} FLAC file(s) in audio/ folder")
    for f in flac_files:
        size_mb = os.path.getsize(os.path.join('audio', f)) / (1024 * 1024)
        print(f"   - {f} ({size_mb:.2f} MB)")

    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n" + "="*60)
    print("Installing Python dependencies...")
    print("="*60)

    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                              capture_output=False, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {str(e)}")
        return False

def main():
    print("="*60)
    print("SETUP AND VALIDATION")
    print("="*60)
    print()

    print("Checking Python version...")
    python_ok = check_python_version()
    print()

    print("Checking FFmpeg...")
    ffmpeg_ok = check_ffmpeg()
    print()

    print("Checking Python packages...")
    packages_ok = check_required_packages()
    print()

    print("Checking .env configuration...")
    env_ok = check_env_file()
    print()

    print("Checking folders...")
    folders_ok = check_folders()
    print()

    print("Checking audio files...")
    audio_ok = check_audio_files()
    print()

    print("="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    checks = {
        "Python 3.8+": python_ok,
        "FFmpeg": ffmpeg_ok,
        "Python packages": packages_ok,
        ".env configuration": env_ok,
        "Folders": folders_ok,
        "Audio files": audio_ok,
    }

    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")

    print()

    if not packages_ok:
        response = input("Would you like to install Python dependencies? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                print("\n❌ Failed to install dependencies")
                sys.exit(1)

    all_critical_ok = python_ok and ffmpeg_ok and packages_ok and env_ok

    if all_critical_ok:
        print("\n✅ Setup validation passed!")
        print("\nYou can now run: python chunk_and_transcribe.py")
    else:
        print("\n❌ Setup validation failed!")
        print("Please fix the issues above before running the script.")
        sys.exit(1)

if __name__ == "__main__":
    main()

