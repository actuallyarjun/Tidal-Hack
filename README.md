# 🔴 Live Navigation MVP

Real-time object detection for navigation assistance.

---

## 🚀 RUN IT

**Double-click:** `RUN_THIS.bat`

That's it! Browser opens, click START button, allow camera.

---

## ✅ What You Get

- Live webcam with real-time object detection
- Bounding boxes around objects
- Distance estimation (red=close, green=far)
- Continuous monitoring

---

## 🐛 If It Doesn't Work

### Test 1: Check packages
```bash
python diagnose.py
```

Should say "[OK] ALL PACKAGES FOUND"

If not, run:
```bash
pip install av streamlit-webrtc ultralytics
```

### Test 2: Simple test
```bash
python -m streamlit run test_livestream.py
```

Should show your webcam with text overlay.

### Test 3: Full app
```bash
python -m streamlit run livestream_simple.py
```

Should show webcam with object detection.

---

## 📁 Files That Matter

- `RUN_THIS.bat` ← **Start here!**
- `livestream_simple.py` ← Main app (350 lines, all-in-one)
- `test_livestream.py` ← Simple test (no detection)
- `diagnose.py` ← Check if packages installed

---

## 🎯 For Hackathon

1. Run `RUN_THIS.bat`
2. Click START
3. Point camera at objects
4. Show real-time detection
5. Demo complete!

---

## ❓ Still Having Issues?

**Tell me EXACTLY what happens:**
- Does the browser open?
- Do you see the START button?
- What happens when you click START?
- Any error messages?

Common issues:
- **Nothing happens**: Check if another app is using camera
- **START doesn't work**: Try Chrome browser, refresh page (F5)
- **No detection**: YOLOv8 model not downloaded, run `python scripts/download_models.py`
