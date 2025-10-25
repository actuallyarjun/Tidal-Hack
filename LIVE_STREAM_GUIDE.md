# 📹 Live Webcam Stream Guide

## ✨ NEW FEATURE: Real-Time Camera Stream

Your Vision Navigation Assistant now supports **continuous real-time video streaming** with live object detection!

---

## 🎯 Three Modes Available

### 1. 🔴 **Live Webcam Stream** (NEW!)
- **Continuous real-time detection**
- Objects detected every frame
- Lowest latency for navigation
- Perfect for real-world use
- **Best for: Live navigation assistance**

### 2. 📸 **Webcam Snapshot**
- Capture single frames on demand
- Manual trigger for analysis
- Good for testing
- **Best for: Step-by-step analysis**

### 3. 📁 **Upload Image**
- Static image analysis
- Test with any photo
- No camera needed
- **Best for: Testing/demo**

---

## 🚀 How to Use Live Stream Mode

### Step 1: Start the App
```bash
streamlit run src/ui/app.py
```

### Step 2: Select Mode
1. In the **sidebar**, select **"Live Webcam Stream"**
2. Click the **"START"** button that appears

### Step 3: Grant Permissions
- Your browser will ask for camera access
- Click **"Allow"** to grant permission
- (Only needed first time)

### Step 4: See Live Detection!
- Your camera feed appears with **real-time bounding boxes**
- Objects are detected continuously
- Distances updated every frame
- Color-coded by safety level:
  - 🔴 Red: <1m (Critical!)
  - 🟠 Orange: 1-1.5m (Warning)
  - 🟡 Yellow: 1.5-3m (Caution)
  - 🟢 Green: >3m (Safe)

### Step 5: Ask Questions
- Detection runs automatically
- **Right sidebar** shows latest objects
- Type questions in the **query box**
- Get AI responses based on live scene

---

## 🎮 Controls

```
┌─────────────────────────────────────────┐
│  START   - Begin camera stream         │
│  STOP    - End camera stream           │
│  Settings (⚙) - Adjust parameters     │
└─────────────────────────────────────────┘
```

---

## 💡 Live Stream Features

### Real-Time Metrics
Displayed on video overlay:
- **Latency**: Detection time per frame
- **FPS**: Frames processed per second
- **Objects**: Count of detected objects

### Safety Monitoring
- Automatic alerts for close objects
- Continuous distance tracking
- Position awareness (left/center/right)
- Haptic feedback triggers

### Query Interface
- Ask questions while stream is active
- Responses based on latest detection
- Conversation history maintained
- Audio feedback (if TTS enabled)

---

## ⚙️ Performance Tuning

### For Best Performance:

```python
# In config/settings.py or .env

# Reduce detection frequency if laggy
TARGET_FPS=15  # Lower FPS = faster processing

# Adjust confidence threshold
CONFIDENCE_THRESHOLD=0.6  # Higher = fewer false detections

# Use smaller image size
# (Set in render_video_feed - already optimized to 1280x720)
```

### Expected Performance:

| Hardware | FPS | Latency |
|----------|-----|---------|
| Modern Laptop (i7) | 15-25 | 40-60ms |
| Gaming PC (i9+GPU) | 25-30 | 30-40ms |
| Older Laptop (i5) | 10-15 | 70-100ms |

---

## 🔧 Troubleshooting

### Issue: "Camera not accessible"

**Solution 1**: Grant browser permissions
- Click the 🔒 lock icon in address bar
- Allow camera access

**Solution 2**: Check other apps
- Close Zoom, Teams, Skype, etc.
- Only one app can use camera at a time

**Solution 3**: Try different browser
- Chrome/Edge work best
- Firefox also supported
- Safari may have issues

### Issue: Stream is laggy

**Solution 1**: Reduce quality
```python
# In render_video_feed, change to:
"video": {
    "width": {"ideal": 640},   # Lower resolution
    "height": {"ideal": 480},
}
```

**Solution 2**: Lower FPS target
```python
# In config/settings.py
TARGET_FPS=10  # Slower but more responsive
```

**Solution 3**: Close other applications
- Free up CPU/memory
- Close background processes

### Issue: "START button does nothing"

**Solutions**:
1. Refresh the page (F5)
2. Clear browser cache
3. Check browser console for errors (F12)
4. Try incognito/private mode

### Issue: Stream freezes

**Solutions**:
1. Click STOP, wait 2 seconds, click START again
2. Refresh the page
3. Check internet connection (needed for STUN server)

---

## 🌟 Use Cases

### Navigation Assistant
```
1. Start live stream
2. Point camera at path ahead
3. Ask: "Is it safe to walk forward?"
4. Get real-time guidance
5. Move slowly while monitoring
```

### Object Finder
```
1. Start live stream
2. Sweep camera around room
3. Ask: "Where is the chair?"
4. System identifies location
5. Audio guides you to object
```

### Environment Scan
```
1. Start live stream
2. Rotate 360 degrees slowly
3. Ask: "Describe my surroundings"
4. Get comprehensive scene description
5. Build mental map of space
```

---

## 🎯 Tips for Best Results

### Camera Positioning
✅ **DO:**
- Hold camera at chest height
- Point straight ahead
- Keep camera steady
- Ensure good lighting

❌ **DON'T:**
- Shake camera rapidly
- Point at ceiling/floor only
- Block lens with fingers
- Use in complete darkness

### Query Timing
- **Wait 1-2 seconds** after stream starts
- Objects need time to be detected
- Check sidebar for object count
- Ask questions when objects appear

### Battery & Performance
- Live stream uses more CPU
- Laptop battery drains faster
- Close other apps to save power
- Use "Webcam Snapshot" mode to save battery

---

## 📊 Live vs Snapshot vs Upload

| Feature | Live Stream | Snapshot | Upload |
|---------|-------------|----------|--------|
| Real-time | ✅ Yes | ❌ No | ❌ No |
| Continuous | ✅ Yes | ❌ No | ❌ No |
| Camera needed | ✅ Yes | ✅ Yes | ❌ No |
| Best latency | ✅ <100ms | ⚡ ~200ms | ⏱️ ~500ms |
| Battery usage | 🔋🔋🔋 High | 🔋🔋 Med | 🔋 Low |
| Navigation | ⭐⭐⭐ Best | ⭐⭐ Good | ⭐ Testing |
| Demo-friendly | ⭐⭐⭐ Best | ⭐⭐ Good | ⭐⭐⭐ Best |

---

## 🎥 Architecture: How Live Stream Works

```
Your Webcam
    ↓
Browser captures frame (30 FPS)
    ↓
WebRTC sends to Streamlit
    ↓
VideoProcessor.recv() called
    ↓
YOLO detects objects (<50ms)
    ↓
Distance estimated (<5ms)
    ↓
Annotated frame rendered
    ↓
Sent back to browser
    ↓
Displayed in real-time
    ↓
(Loop continuously)

Meanwhile:
- Latest detection stored in session
- Sidebar updates automatically
- Queries processed on latest frame
- Audio feedback can interrupt
```

---

## 🚀 Next Steps

### Try These Live Stream Tests:

**Test 1: Object Tracking** (30 seconds)
1. Start live stream
2. Place object in view
3. Move object left/right
4. Watch bounding box follow it
5. Note distance changes

**Test 2: Distance Accuracy** (1 minute)
1. Start live stream
2. Point at known object (e.g., door)
3. Note estimated distance
4. Measure actual distance
5. Compare accuracy (±20% typical)

**Test 3: Safety Alerts** (30 seconds)
1. Start live stream
2. Move hand toward camera
3. Watch color change: Green → Yellow → Red
4. At <1m, should show critical alert
5. Check haptic feedback indicator

**Test 4: Live Queries** (1 minute)
1. Start live stream
2. Ask: "What do you see?"
3. Get description of current frame
4. Move camera to new scene
5. Ask again, see updated response

---

## 💾 Recording & Screenshots

### To Record Stream:
```
(Currently not built-in)

Options:
1. Use OBS Studio to record
2. Use built-in screen recording
3. Browser extensions (Loom, etc.)
```

### To Take Screenshots:
1. While stream is active
2. Press Windows: Win+PrintScreen
3. Or use Snipping Tool
4. Captured frame saved to Pictures

---

## 🎓 For Developers

### Customizing the Video Processor:

```python
# In src/ui/app.py

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        # ADD YOUR CUSTOM PROCESSING HERE
        # Example: Apply filters, run additional models, etc.
        
        annotated_frame, detections = self.detector.detect(img)
        
        # MODIFY OUTPUT HERE
        # Example: Add custom overlays, text, etc.
        
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
```

### Adjusting Stream Quality:

```python
media_stream_constraints={
    "video": {
        "width": {"ideal": 1920},    # 1080p
        "height": {"ideal": 1080},
        "frameRate": {"ideal": 30},  # Max FPS
    },
    "audio": False
}
```

---

## ✅ Quick Reference

```
START STREAM:
  streamlit run src/ui/app.py
  → Select "Live Webcam Stream"
  → Click START
  → Allow camera access

STOP STREAM:
  → Click STOP button
  → Or refresh page

TROUBLESHOOT:
  → Check camera permissions
  → Close other camera apps
  → Try different browser
  → Reduce video quality

ASK QUESTIONS:
  → Type in query box
  → Press Send
  → Get real-time response
```

---

## 🎉 You're Ready!

**Live stream mode is now active!**

Try it out:
1. Run: `streamlit run src/ui/app.py`
2. Select: "Live Webcam Stream"
3. Click: "START"
4. Experience: Real-time navigation!

**Perfect for hackathon demos!** 🚀

