# Installation Guide

## Step-by-Step Installation for Python 3.13

### Step 1: Install Core Dependencies

```bash
# Install core packages first
pip install --upgrade pip setuptools wheel

# Install essential packages
pip install numpy
pip install opencv-python
pip install pillow
pip install pydantic pydantic-settings
pip install python-dotenv
pip install requests
```

### Step 2: Install PyTorch (choose one based on your system)

**Option A: CPU Only (Faster download, works everywhere)**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**Option B: CUDA GPU Support (if you have NVIDIA GPU)**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Step 3: Install Computer Vision

```bash
pip install ultralytics
```

### Step 4: Install Streamlit

```bash
pip install streamlit
```

### Step 5: Install Optional Cloud Services

```bash
# For Gemini VLM (optional)
pip install google-generativeai

# For AWS Bedrock (optional)
pip install boto3 botocore
```

### Step 6: Install Optional Audio Features

**Text-to-Speech (Recommended):**
```bash
pip install pyttsx3
pip install gtts
```

**Voice Input (Advanced - can skip for now):**

Windows:
```bash
pip install pipwin
pipwin install pyaudio
pip install speechrecognition
```

macOS:
```bash
brew install portaudio
pip install pyaudio
pip install speechrecognition
```

Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
pip install speechrecognition
```

## Quick Installation (Skip Audio)

If you want to skip audio features for now:

```bash
# All core features without audio
pip install numpy opencv-python pillow pydantic pydantic-settings python-dotenv requests
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
pip install streamlit
pip install google-generativeai boto3
```

## Verify Installation

```bash
python verify_setup.py
```

## Common Issues

### Issue 1: "error: Microsoft Visual C++ 14.0 or greater is required"

**Solution:** Install Visual Studio Build Tools
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install "Desktop development with C++"

### Issue 2: PyAudio fails to install

**Solution:** Skip audio features for now or use pipwin:
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue 3: Torch installation is very slow

**Solution:** Use CPU-only version:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Issue 4: "No module named 'pydantic_settings'"

**Solution:**
```bash
pip install pydantic-settings
```

### Issue 5: Python 3.13 compatibility issues

**Solution:** Some packages might not have Python 3.13 wheels yet. You can:
1. Use Python 3.11 or 3.12 instead (recommended for hackathon)
2. Wait for package updates
3. Skip problematic optional packages

## Minimal Installation (Just to test)

To get started quickly with core features only:

```bash
pip install streamlit opencv-python numpy pillow pydantic pydantic-settings python-dotenv
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
```

This gives you:
- ✅ Object detection
- ✅ Distance estimation
- ✅ Web UI
- ✅ Image upload/webcam
- ✅ Mock agent responses
- ❌ No Gemini VLM
- ❌ No AWS Bedrock
- ❌ No audio features

**This is enough to demo the system!**

## After Installation

1. Download YOLO model:
```bash
python scripts/download_models.py
```

2. Run the app:
```bash
streamlit run src/ui/app.py
```

## Need Help?

**Share the specific error message** and I can provide a targeted fix!

Common patterns:
- `error: Microsoft Visual C++` → Install Build Tools
- `Could not find a version` → Package not available for Python 3.13
- `No module named 'pydantic_settings'` → `pip install pydantic-settings`
- PyAudio errors → Skip audio for now, system works without it

