"""
Verification script to check if all components are properly installed.
"""
import sys
from pathlib import Path

# Use ASCII-compatible check marks for Windows compatibility
CHECK_MARK = "[OK]"
CROSS_MARK = "[!!]"
OPTIONAL_MARK = "[--]"

print("=" * 60)
print("Vision Navigation Assistant - Setup Verification")
print("=" * 60)
print()

# Track overall status
all_good = True

# 1. Check Python version
print("1. Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"   {CHECK_MARK} Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"   {CROSS_MARK} Python {sys.version_info.major}.{sys.version_info.minor} (requires 3.8+)")
    all_good = False
print()

# 2. Check core dependencies
print("2. Checking core dependencies...")
required_packages = {
    'streamlit': 'Streamlit',
    'cv2': 'OpenCV',
    'numpy': 'NumPy',
    'PIL': 'Pillow',
    'pydantic': 'Pydantic',
}

for module, name in required_packages.items():
    try:
        __import__(module)
        print(f"   {CHECK_MARK} {name}")
    except ImportError:
        print(f"   {CROSS_MARK} {name} - Run: pip install -r requirements.txt")
        all_good = False
print()

# 3. Check YOLO
print("3. Checking YOLO/Ultralytics...")
try:
    from ultralytics import YOLO
    print(f"   {CHECK_MARK} Ultralytics installed")
except ImportError:
    print(f"   {CROSS_MARK} Ultralytics - Run: pip install ultralytics")
    all_good = False
print()

# 4. Check optional dependencies
print("4. Checking optional dependencies...")

# Gemini
try:
    import google.generativeai as genai
    print(f"   {CHECK_MARK} Google Generative AI (Gemini support)")
except ImportError:
    print(f"   {OPTIONAL_MARK} Google Generative AI (optional) - Install: pip install google-generativeai")

# AWS
try:
    import boto3
    print(f"   {CHECK_MARK} Boto3 (AWS support)")
except ImportError:
    print(f"   {OPTIONAL_MARK} Boto3 (optional) - Install: pip install boto3")

# Audio
try:
    import pyttsx3
    print(f"   {CHECK_MARK} pyttsx3 (Text-to-Speech)")
except ImportError:
    print(f"   {OPTIONAL_MARK} pyttsx3 (optional) - Install: pip install pyttsx3")

try:
    import speech_recognition
    print(f"   {CHECK_MARK} SpeechRecognition (Voice input)")
except ImportError:
    print(f"   {OPTIONAL_MARK} SpeechRecognition (optional) - Install: pip install speechrecognition pyaudio")

print()

# 5. Check configuration
print("5. Checking configuration...")
try:
    from config.settings import settings
    print(f"   {CHECK_MARK} Configuration loaded")
    
    # Check feature status
    feature_status = settings.get_feature_status()
    
    if feature_status['gemini_api']:
        print(f"   {CHECK_MARK} Gemini API key configured")
    else:
        print(f"   {OPTIONAL_MARK} Gemini API key not configured (using mock mode)")
    
    if feature_status['aws_credentials']:
        print(f"   {CHECK_MARK} AWS credentials configured")
    else:
        print(f"   {OPTIONAL_MARK} AWS credentials not configured (using local mode)")
        
except Exception as e:
    print(f"   {CROSS_MARK} Configuration error: {e}")
    all_good = False
print()

# 6. Check project structure
print("6. Checking project structure...")
required_dirs = [
    'config',
    'src/cv_engine',
    'src/cloud_agent',
    'src/audio',
    'src/ui',
    'scripts'
]

for dir_path in required_dirs:
    if Path(dir_path).exists():
        print(f"   {CHECK_MARK} {dir_path}/")
    else:
        print(f"   {CROSS_MARK} {dir_path}/ - Missing directory")
        all_good = False
print()

# 7. Check YOLO model
print("7. Checking YOLO model...")
model_path = Path("src/cv_engine/models/yolov8n.pt")
if model_path.exists():
    print(f"   {CHECK_MARK} YOLO model found at {model_path}")
else:
    print(f"   {OPTIONAL_MARK} YOLO model not found - Run: python scripts/download_models.py")
print()

# 8. Test imports
print("8. Testing module imports...")
try:
    from src.cv_engine.detector import ObjectDetector
    print(f"   {CHECK_MARK} CV Engine")
except Exception as e:
    print(f"   {CROSS_MARK} CV Engine - {e}")
    all_good = False

try:
    from src.cloud_agent.local_agent import LocalNavigationAgent
    print(f"   {CHECK_MARK} Cloud Agent")
except Exception as e:
    print(f"   {CROSS_MARK} Cloud Agent - {e}")
    all_good = False

try:
    from src.audio.tts_output import TTSEngine
    print(f"   {CHECK_MARK} Audio Module")
except Exception as e:
    print(f"   {CROSS_MARK} Audio Module - {e}")
    all_good = False

try:
    from src.ui.app import main
    print(f"   {CHECK_MARK} UI Module")
except Exception as e:
    print(f"   {CROSS_MARK} UI Module - {e}")
    all_good = False

print()

# Final summary
print("=" * 60)
if all_good:
    print("[OK] ALL CHECKS PASSED!")
    print()
    print("You're ready to run the application:")
    print("  streamlit run src/ui/app.py")
    print()
    print("Or use the quick start script:")
    print("  Windows: run_app.bat")
    print("  macOS/Linux: ./run_app.sh")
else:
    print("[!!] SOME CHECKS FAILED")
    print()
    print("Please fix the issues above and run this script again.")
    print()
    print("Quick fixes:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Download YOLO model: python scripts/download_models.py")

print("=" * 60)

