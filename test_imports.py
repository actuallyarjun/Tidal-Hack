"""
Quick diagnostic to check what's actually happening with imports
"""
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")
print()

# Test 1: av
print("=" * 60)
print("TEST 1: Importing 'av'")
print("=" * 60)
try:
    import av
    print(f"[OK] SUCCESS: av version {av.__version__}")
    print(f"     Location: {av.__file__}")
except ImportError as e:
    print(f"[NO] FAILED: {e}")
except Exception as e:
    print(f"[ERR] ERROR: {e}")
print()

# Test 2: streamlit_webrtc
print("=" * 60)
print("TEST 2: Importing 'streamlit_webrtc'")
print("=" * 60)
try:
    import streamlit_webrtc
    print(f"[OK] SUCCESS: streamlit_webrtc imported")
    print(f"     Location: {streamlit_webrtc.__file__}")
    
    # Test specific imports
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    print(f"[OK] All components imported successfully")
except ImportError as e:
    print(f"[NO] FAILED: {e}")
except Exception as e:
    print(f"[ERR] ERROR: {e}")
print()

# Test 3: Both together
print("=" * 60)
print("TEST 3: Combined import (as in app)")
print("=" * 60)
WEBRTC_AVAILABLE = False
try:
    import av
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    WEBRTC_AVAILABLE = True
    print(f"[OK] SUCCESS: WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
except ImportError as e:
    print(f"[NO] FAILED: {e}")
    print(f"     WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
except Exception as e:
    print(f"[ERR] ERROR: {e}")
    print(f"      WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
print()

# Test 4: Check if packages are in sys.modules
print("=" * 60)
print("TEST 4: Checking sys.modules")
print("=" * 60)
print(f"'av' in sys.modules: {'av' in sys.modules}")
print(f"'streamlit_webrtc' in sys.modules: {'streamlit_webrtc' in sys.modules}")
print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)
if WEBRTC_AVAILABLE:
    print("[OK] ALL TESTS PASSED - Stream should work!")
else:
    print("[NO] TESTS FAILED - Stream will not work")
    print()
    print("SOLUTION:")
    print(f"  {sys.executable} -m pip install av streamlit-webrtc")

