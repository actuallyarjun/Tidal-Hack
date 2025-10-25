# Camera Calibration Guide

## Why Calibrate?

Different cameras have different focal lengths and fields of view. Calibration ensures accurate distance measurements for YOUR specific camera.

---

## Quick Calibration (2 minutes)

### Method 1: Using a Person (Easiest)

1. **Setup:**
   - Have someone stand exactly **2 meters** (6.5 feet) away
   - Use a tape measure or ruler for accuracy
   - Make sure they're facing the camera

2. **Run the app:**
   ```
   RUN_THIS.bat
   ```

3. **Detect the person:**
   - Point camera at the person
   - App should detect "person" with a box

4. **Note the measured distance:**
   - App will show estimated distance (e.g., "person 3.2m")
   - This is BEFORE calibration

5. **Calculate calibration factor:**
   ```
   Calibration Factor = Actual Distance / Measured Distance
   Example: 2.0m / 3.2m = 0.625
   ```

6. **Update .env file:**
   ```bash
   CALIBRATION_FACTOR=0.625
   ```

7. **Restart app** - Now distances should be accurate!

---

## Method 2: Using a Chair/Object

1. **Measure a chair:**
   - Typical chair height: 0.9m (35 inches)
   - Measure yours to be sure!

2. **Place chair 1.5 meters away:**
   - Use tape measure
   - Place in center of camera view

3. **Follow steps 2-7 above**

---

## Method 3: Auto-Calibration in UI (Coming Soon)

The app will have a calibration wizard:
- Point at reference object
- Enter actual distance
- Click "Calibrate"
- Done!

---

## Understanding Camera Parameters

### Focal Length (in pixels)
- **What it is:** How "zoomed in" your camera is
- **Typical values:**
  - Webcam (720p): 600-700 pixels
  - Webcam (480p): 400-500 pixels
  - Phone camera: 700-900 pixels
- **Auto-detected:** App estimates this based on resolution

### Field of View (FOV)
- **Webcam:** Usually 60-70 degrees
- **Phone front camera:** 70-80 degrees
- **Phone back camera:** 75-85 degrees
- **Wide-angle webcam:** 90+ degrees

---

## Device-Specific Notes

### Laptop Webcams
- Usually 720p or 1080p
- FOV: ~70 degrees
- **Calibration factor:** Usually 0.8-1.2

### External USB Webcams
- Varies widely
- Check manufacturer specs
- **Calibration factor:** Usually 0.7-1.3

### Phone Cameras (via browser)
- Higher quality, better accuracy
- Front camera: Wider FOV
- **Calibration factor:** Usually 0.9-1.1

### Tablets
- Similar to phones
- Larger screen = easier to see
- **Calibration factor:** Usually 0.9-1.1

---

## Troubleshooting

### Distances Too Large
- **Problem:** App says 5m, actually 2m
- **Fix:** Calibration factor should be LESS than 1.0
- **Example:** Factor = 0.4 (2m / 5m)

### Distances Too Small
- **Problem:** App says 1m, actually 3m  
- **Fix:** Calibration factor should be MORE than 1.0
- **Example:** Factor = 3.0 (3m / 1m)

### Distances Wildly Wrong
- **Check:**
  - Is object detected correctly?
  - Is lighting good?
  - Is object fully visible (not cut off)?
- **Try:** Different reference object

### Distances Vary by Position
- **Normal:** Center of frame more accurate
- **Why:** Lens distortion at edges
- **Fix:** Use objects in center for calibration

---

## Advanced: Manual Focal Length Calculation

If you know your camera specs:

```
Focal Length (pixels) = (Focal Length mm / Sensor Height mm) × Image Height (pixels)

Example (typical webcam):
- Focal Length: 3.6mm
- Sensor Height: 4.8mm  
- Image Height: 720 pixels

Focal Length (pixels) = (3.6 / 4.8) × 720 = 540 pixels
```

Add to `.env`:
```bash
FOCAL_LENGTH_MM=3.6
SENSOR_HEIGHT_MM=4.8
```

---

## Testing Calibration

### Quick Test:
1. Stand 1 meter from camera
2. App should show ~1.0m
3. Walk to 2 meters
4. App should show ~2.0m
5. Repeat with different objects

### Accuracy Goals:
- **Good:** ±20% error (1.6-2.4m for 2m actual)
- **Excellent:** ±10% error (1.8-2.2m for 2m actual)
- **Perfect:** ±5% error (1.9-2.1m for 2m actual)

**For navigation assistance, "Good" is sufficient!**

---

## Current System Defaults

The app uses **adaptive estimation**:

```python
Resolution  → Default Focal Length (pixels)
720p        → 650 (height × 0.9)
480p        → 480 (height × 1.0)  
360p        → 432 (height × 1.2)
```

This works reasonably well WITHOUT calibration but calibration improves accuracy significantly.

---

## Quick Reference

**Best Reference Objects:**
- ✅ Person (1.7m tall) at 2m distance
- ✅ Chair (0.9m tall) at 1.5m distance
- ✅ Door (2.0m tall) at 3m distance
- ❌ Small objects (too variable)
- ❌ Reflective objects (detection issues)

**Tools Needed:**
- Tape measure or ruler
- Calculator (or use phone)
- 2 minutes of time

**When to Recalibrate:**
- Different camera
- Different room (lighting)
- After app updates
- If distances seem wrong

---

## Summary

1. ✅ **Without calibration:** Distances are approximate (±30% error)
2. ✅ **With calibration:** Distances are accurate (±10% error)
3. ✅ **Calibration takes 2 minutes**
4. ✅ **Only needs to be done once per camera**

**For hackathon demo: Use default settings, they're "good enough"!**

**For real-world use: Calibrate for best accuracy!**

