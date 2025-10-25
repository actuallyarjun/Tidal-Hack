# Cross-Platform Setup Guide

Complete setup instructions for **Windows**, **macOS**, and **Linux**.

---

## 🪟 Windows Setup

### Quick Start

1. **Install Python 3.8+** (if not installed)
   - Download from: https://python.org
   - ✅ Check "Add Python to PATH" during installation

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```cmd
   Double-click: RUN_THIS.bat
   ```

### Alternative: Manual Run
```cmd
python -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### PyAudio Installation (Windows)

If you get microphone errors:

**Option 1: pip (Python 3.13 works!):**
```cmd
pip install pyaudio
```

**Option 2: If pip fails, use pipwin:**
```cmd
pip install pipwin
pipwin install pyaudio
```

**Option 3: Pre-built wheel:**
Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

---

## 🍎 macOS Setup

### Quick Start

1. **Install Python 3.8+** (if not installed)
   ```bash
   # Using Homebrew (recommended)
   brew install python3
   ```

2. **Install system dependencies:**
   ```bash
   # For PyAudio
   brew install portaudio
   
   # For OpenCV
   brew install opencv
   ```

3. **Install Python packages:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Make script executable:**
   ```bash
   chmod +x RUN_THIS.sh
   ```

5. **Run the app:**
   ```bash
   ./RUN_THIS.sh
   ```

### Alternative: Manual Run
```bash
python3 -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### PyAudio Installation (macOS)

```bash
brew install portaudio
pip3 install pyaudio
```

If you get compilation errors:
```bash
export CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib"
pip3 install pyaudio
```

---

## 🐧 Linux Setup

### Quick Start (Ubuntu/Debian)

1. **Install Python 3.8+** (usually pre-installed)
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install system dependencies:**
   ```bash
   # For PyAudio
   sudo apt install portaudio19-dev python3-pyaudio
   
   # For OpenCV
   sudo apt install libgl1-mesa-glx libglib2.0-0
   
   # For TTS (optional)
   sudo apt install espeak
   ```

3. **Install Python packages:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Make script executable:**
   ```bash
   chmod +x RUN_THIS.sh
   ```

5. **Run the app:**
   ```bash
   ./RUN_THIS.sh
   ```

### Alternative: Manual Run
```bash
python3 -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### PyAudio Installation (Linux)

```bash
sudo apt install portaudio19-dev
pip3 install pyaudio
```

For other distros:
```bash
# Fedora/RHEL
sudo dnf install portaudio-devel
pip3 install pyaudio

# Arch
sudo pacman -S portaudio
pip3 install pyaudio
```

---

## 📁 Files for Each Platform

| Platform | Launcher | Debug Launcher |
|----------|----------|----------------|
| Windows  | `RUN_THIS.bat` | `DEBUG_RUN.bat` |
| macOS    | `RUN_THIS.sh` | `DEBUG_RUN.sh` |
| Linux    | `RUN_THIS.sh` | `DEBUG_RUN.sh` |

---

## 🔧 Common Installation Issues

### Issue: "command not found: python"

**Solution:**
- Windows: Add Python to PATH, reinstall Python
- macOS/Linux: Try `python3` instead of `python`

### Issue: "Permission denied" (macOS/Linux)

**Solution:**
```bash
chmod +x RUN_THIS.sh
chmod +x DEBUG_RUN.sh
```

### Issue: PyAudio won't install

**Windows:**
```cmd
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip3 install pyaudio
```

**Linux:**
```bash
sudo apt install portaudio19-dev
pip3 install pyaudio
```

### Issue: "cv2 not found" or OpenCV errors

**All platforms:**
```bash
pip install opencv-python
```

**Linux (additional):**
```bash
sudo apt install libgl1-mesa-glx libglib2.0-0
```

### Issue: TTS not working

**Windows:** Should work out of box with pyttsx3

**macOS:**
```bash
pip3 install pyttsx3
# Uses built-in macOS speech
```

**Linux:**
```bash
sudo apt install espeak
pip3 install pyttsx3
```

---

## 🌐 Network Access (All Platforms)

### Find Your Local IP

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Linux:**
```bash
hostname -I
```
or
```bash
ip addr show
```

### Access URLs

**From your computer:**
- `http://localhost:8501`
- `http://127.0.0.1:8501`

**From phone/tablet (same WiFi):**
- `http://YOUR_LOCAL_IP:8501`
- Example: `http://192.168.1.100:8501`

---

## 🎤 Voice Command Setup

### Windows
1. Install: `pip install pyaudio SpeechRecognition`
2. Allow microphone access in Windows Settings
3. Restart app

### macOS
1. Install: `brew install portaudio && pip3 install pyaudio SpeechRecognition`
2. Grant microphone permission when prompted
3. System Preferences → Security & Privacy → Microphone → Allow Terminal/Browser

### Linux
1. Install: `sudo apt install portaudio19-dev && pip3 install pyaudio SpeechRecognition`
2. Check microphone: `arecord -l`
3. Test: `arecord -d 3 test.wav && aplay test.wav`

---

## 🤖 Gemini AI Setup (All Platforms)

1. Get API key: https://makersuite.google.com/app/apikey

2. Create `.env` file:
   ```bash
   # Windows
   copy env.example .env
   
   # macOS/Linux
   cp env.example .env
   ```

3. Edit `.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   USE_GEMINI=true
   ```

4. Restart app

---

## 📊 System Requirements

### Minimum:
- **OS:** Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python:** 3.8+
- **RAM:** 4GB
- **Disk:** 2GB free space
- **Camera:** Built-in or USB webcam
- **Microphone:** For voice commands

### Recommended:
- **Python:** 3.10+
- **RAM:** 8GB+
- **CPU:** Multi-core for better performance
- **Internet:** For Gemini AI and speech recognition

---

## 🧪 Testing Your Setup

### Test 1: Import Test
```bash
# Windows
python test_imports.py

# macOS/Linux
python3 test_imports.py
```

Expected: `[OK] ALL TESTS PASSED`

### Test 2: Launch App
```bash
# Windows
RUN_THIS.bat

# macOS/Linux
./RUN_THIS.sh
```

Expected: Browser opens to localhost:8501

### Test 3: Voice Commands
1. Click "🎤 Voice" button
2. Speak: "What do you see?"
3. Get response (text + audio)

Expected: Recognition works, TTS speaks

### Test 4: Network Access
1. Note your local IP from terminal
2. On phone, go to `http://YOUR_IP:8501`
3. See same app

Expected: Works from phone

---

## 📝 Quick Command Reference

### Windows
```cmd
# Install dependencies
pip install -r requirements.txt

# Run app
RUN_THIS.bat

# Debug mode
DEBUG_RUN.bat

# Manual run
python -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### macOS/Linux
```bash
# Install dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x *.sh

# Run app
./RUN_THIS.sh

# Debug mode
./DEBUG_RUN.sh

# Manual run
python3 -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

---

## 🆘 Getting Help

If you encounter issues:

1. Check **FINAL_FIX_SUMMARY.txt** for common fixes
2. Check **STREAM_FIX.txt** for stream issues
3. Check **CALIBRATION_GUIDE.md** for camera setup
4. Check terminal output for specific errors

**Most common fix:** Restart the app!

---

## ✅ Success Checklist

- [ ] Python installed and in PATH
- [ ] Dependencies installed (`requirements.txt`)
- [ ] PyAudio working (microphone access)
- [ ] Streamlit launches without errors
- [ ] Browser opens to localhost:8501
- [ ] Live stream shows "🔴 Live Stream Ready!"
- [ ] Camera works (click START)
- [ ] Object detection working
- [ ] Voice commands work (optional)
- [ ] Gemini AI configured (optional)
- [ ] Network access from phone (optional)

---

**All platforms fully supported!** Choose your platform and follow the instructions above.

