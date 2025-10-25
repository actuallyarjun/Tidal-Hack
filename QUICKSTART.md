# 🚀 Quick Start Guide

## For Windows Users

### Option 1: Automated Setup (Easiest)

1. Double-click `run_app.bat`
2. Wait for automatic setup to complete
3. Application will open in your browser

### Option 2: Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download YOLO model
python scripts\download_models.py

# 4. Run the app
streamlit run src\ui\app.py
```

---

## For macOS/Linux Users

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download YOLO model
python scripts/download_models.py

# 4. Run the app
streamlit run src/ui/app.py
```

---

## First Time Usage

1. **No API Keys Needed**: The app works perfectly without any API keys
2. **Select Mode**: Choose "Upload Image" or "Webcam Snapshot" in sidebar
3. **Upload/Capture**: Provide an image for analysis
4. **Ask Questions**: Type questions like "Describe what you see"
5. **Get Responses**: Receive AI-powered navigation assistance

---

## Optional: Adding API Keys

For enhanced features (optional):

1. Copy `env.example` to `.env`
2. Add your API keys:
   - `GEMINI_API_KEY` - For advanced scene understanding
   - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` - For Bedrock
3. Set feature flags to `true`:
   ```
   USE_GEMINI=true
   USE_BEDROCK=true
   MOCK_MODE=false
   ```
4. Restart the application

---

## Troubleshooting

### PyAudio Installation (for voice input)

**Windows:**
```powershell
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Webcam Access Issues

- Grant browser camera permissions
- Close other apps using the camera
- Use "Upload Image" mode instead

### Model Download Fails

```bash
# Manual download
pip install ultralytics
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Check the demo script for hackathon presentations
- Explore the modular architecture for customization

---

**Ready to Navigate! 🎯**

