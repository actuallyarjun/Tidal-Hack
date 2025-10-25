# Vision Navigation Assistant

**Real-time AI-powered navigation for visually impaired users • Powered by Gemini**

Live object detection + voice commands + intelligent scene understanding

---

## Quick Start

### Windows
```
Double-click: RUN_THIS.bat
```

### macOS/Linux
```bash
chmod +x RUN_THIS.sh
./RUN_THIS.sh
```

That's it! Your browser will open automatically.

📖 **Full setup guide:** See `CROSS_PLATFORM_SETUP.md` for detailed instructions

### Network Access (Phone/Tablet)
The app automatically starts with network access enabled. When you run it, you'll see:
```
Access from THIS device: http://localhost:8501
Access from OTHER devices: http://192.168.X.X:8501
```

From any device on **same WiFi**, open the IP address shown!

---

## Features

- **Live webcam stream** - Real-time video processing
- **Object detection** - YOLOv8 identifies obstacles
- **Distance estimation** - Measures in meters
- **Voice commands** - Hands-free questions
- **Gemini AI** - Intelligent scene understanding
- **Text-to-speech** - Spoken responses
- **Safety alerts** - Color-coded warnings
- **Mobile ready** - Access from any device

---

## How to Use

1. **Start the app** → `RUN_THIS.bat`
2. **Click START** → Allow camera access
3. **See live detection** → Objects with distance labels
4. **Ask questions** → Click "🎤 Voice" button
5. **Speak command** → "What do you see?"
6. **Get AI response** → Voice + text feedback

### Example Voice Commands:
- **"Is it safe?"** → Safety check
- **"What do you see?"** → Scene description
- **"Where can I go?"** → Navigation guidance
- **"Find the door"** → Locate objects
- **"Describe ahead"** → Forward view

---

## Setup Gemini AI

### Why Gemini?
Without Gemini, the app uses basic pattern matching. With Gemini, you get:
- Context-aware responses
- Natural conversation
- Spatial understanding
- Intelligent navigation

### Get Started:
1. **Get API key**: https://makersuite.google.com/app/apikey
2. **Copy template**: Copy `env.example` to `.env`
3. **Add your key**:
   ```bash
   GEMINI_API_KEY=your_actual_key_here
   USE_GEMINI=true
   ```
4. **Restart app**

**Check Status**: App shows "✓ Gemini AI" when working!

---

## Requirements

- Python 3.8+ (tested on 3.13)
- Webcam
- Microphone (for voice)
- Windows/Linux/macOS

**Auto-installed** by `RUN_THIS.bat`:
- `streamlit-webrtc` - Live streaming
- `av` - Video processing
- `ultralytics` - YOLOv8
- `google-generativeai` - Gemini AI
- `speechrecognition` - Voice input
- `pyttsx3` - Text-to-speech

---

## Color Coding

Objects are highlighted by distance:
- **Red** < 1.5m → DANGER - Stop!
- **Orange** 1.5-3m → CAUTION
- **Green** > 3m → SAFE

---

## Mobile Access

1. Run `RUN_THIS.bat` on laptop
2. Note IP address in terminal
3. On phone:
   - Connect to **SAME WiFi**
   - Open browser
   - Go to `http://YOUR_IP:8501`
4. See live stream!

**Works on**: iPhone, Android, tablets, other laptops

---

## Troubleshooting

### Live Stream
- **No video?** → Allow camera in browser
- **Error?** → Close other apps using camera
- **Module not found?** → `pip install av streamlit-webrtc`

### Voice Commands
- **Unavailable?** → `pip install pyaudio SpeechRecognition`
- **Not hearing?** → Check mic permissions
- **Recognition fails?** → Speak clearly, check internet

### Gemini AI
- **"Basic Mode"?** → Add `GEMINI_API_KEY` to `.env`
- **API errors?** → Check internet, verify key
- **Rate limits?** → Free tier limits, wait briefly

### Network Access
- **Can't connect?** → Same WiFi? Check firewall (allow port 8501)
- **Wrong IP?** → Use IP from terminal, not random
- **Still fails?** → Try `http://` not `https://`

---

## Project Structure

```
Tidal-Hack/
├── RUN_THIS.bat           # Main launcher
├── .env                    # Your Gemini API key
├── env.example             # Template for .env
├── requirements.txt        # Dependencies
├── config/
│   └── settings.py         # Configuration (Gemini-focused)
└── src/
    ├── cv_engine/          # Object detection & distance
    ├── cloud_agent/        # Gemini AI integration
    │   ├── local_agent.py     # Main orchestrator
    │   ├── gemini_tool.py     # Gemini API wrapper
    │   ├── tools.py           # Navigation helpers
    │   └── mock_responses.py  # Fallback when no API
    ├── audio/              # Voice I/O
    │   ├── tts_output.py      # Text-to-speech
    │   └── speech_input.py    # Speech recognition
    └── ui/
        └── app.py          # Streamlit interface
```

---

## Architecture

### Modular Design:
```
Webcam → CV Engine → Local Agent → Gemini AI
                          ↓
                    Voice + TTS
```

### Components:
- **CV Engine**: YOLOv8 detection + distance estimation
- **Local Agent**: Orchestrates all components
- **Gemini AI**: Scene understanding + navigation
- **Audio**: Voice input + TTS output
- **UI**: Streamlit web interface

### Why This Structure?
- **Clean separation** of concerns
- **Easy to extend** with new features
- **Testable** individual components
- **Maintainable** codebase
- **Gemini-powered** intelligence

---

## For Hackathon

**Demo Flow** (3 minutes):
1. **Show live detection** (30s)
   - Point camera at objects
   - Show color-coded boxes
   
2. **Voice interaction** (1min)
   - "Is it safe?"
   - "What do you see?"
   - Show AI response + TTS
   
3. **Mobile access** (30s)
   - Show same stream on phone
   - Demonstrate portability
   
4. **Explain impact** (1min)
   - Real independence for blind users
   - Hands-free operation
   - Context-aware guidance

**Key Points**:
- ✅ Actually useful technology
- ✅ Real-time processing
- ✅ AI-powered intelligence
- ✅ Mobile accessible
- ✅ Voice controlled

---

## Future Enhancements

- [ ] GPS integration for outdoor navigation
- [ ] Route planning with Google Maps
- [ ] Haptic feedback via phone
- [ ] Offline mode with local models
- [ ] Cloud deployment (AWS/GCP)
- [ ] Native mobile app
- [ ] Multi-language support

---

## License

See LICENSE file for details.

---

**Built for accessibility. Powered by Gemini AI. Ready to demo! 🎉**

---

## Acknowledgments

- **Google Gemini** for intelligent AI
- **YOLOv8** for object detection
- **Streamlit** for rapid prototyping
- **Community** for accessibility focus
