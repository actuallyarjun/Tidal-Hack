"""
Test script to verify speech recognition works
Run this BEFORE running the main app
"""
import sys

print("=" * 60)
print("SPEECH RECOGNITION TEST")
print("=" * 60)
print()

# Test 1: PyAudio
print("TEST 1: PyAudio")
print("-" * 60)
try:
    import pyaudio
    print("[OK] PyAudio is installed")
    print(f"     Version: {pyaudio.__version__}")
    
    # Try to create PyAudio instance
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    print(f"[OK] Found {device_count} audio devices")
    
    # List microphones
    print("\n     Available input devices:")
    for i in range(device_count):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"       - {info['name']}")
    
    p.terminate()
    pyaudio_ok = True
except ImportError:
    print("[NO] PyAudio NOT installed")
    print("     Install with: pip install pyaudio")
    pyaudio_ok = False
except Exception as e:
    print(f"[ERR] PyAudio error: {e}")
    pyaudio_ok = False

print()

# Test 2: SpeechRecognition
print("TEST 2: SpeechRecognition")
print("-" * 60)
try:
    import speech_recognition as sr
    print("[OK] SpeechRecognition is installed")
    print(f"     Version: {sr.__version__}")
    speech_ok = True
except ImportError:
    print("[NO] SpeechRecognition NOT installed")
    print("     Install with: pip install SpeechRecognition")
    speech_ok = False
except Exception as e:
    print(f"[ERR] Error: {e}")
    speech_ok = False

print()

# Test 3: Full integration test
if pyaudio_ok and speech_ok:
    print("TEST 3: Full Speech Recognition Test")
    print("-" * 60)
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print("[OK] Microphone initialized")
        print()
        print("Adjusting for ambient noise...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("[OK] Calibration complete")
        print()
        print("=" * 60)
        print("LIVE TEST - Speak now!")
        print("=" * 60)
        print("Say something like: 'testing one two three'")
        print("You have 5 seconds...")
        print()
        
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        
        print()
        print("=" * 60)
        print(f"SUCCESS! Recognized: '{text}'")
        print("=" * 60)
        print()
        print("[OK] Speech recognition is working!")
        print("[OK] Voice button should work in the app!")
        
    except sr.WaitTimeoutError:
        print("[WARN] No speech detected within timeout")
        print("       Try again with louder voice")
    except sr.UnknownValueError:
        print("[WARN] Could not understand audio")
        print("       Try speaking more clearly")
    except sr.RequestError as e:
        print(f"[ERR] Google Speech API error: {e}")
        print("      Check internet connection")
    except Exception as e:
        print(f"[ERR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("TEST 3: SKIPPED (missing dependencies)")
    print("-" * 60)

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

if pyaudio_ok and speech_ok:
    print("[OK] All packages installed")
    print("[OK] Speech recognition should work in the app")
    print()
    print("Next steps:")
    print("  1. Run: RUN_THIS.bat")
    print("  2. Check sidebar: Should show 'Speech: Enabled ✓'")
    print("  3. Click voice button and speak")
else:
    print("[NO] Missing packages:")
    if not pyaudio_ok:
        print("  - PyAudio")
    if not speech_ok:
        print("  - SpeechRecognition")
    print()
    print("Fix with:")
    print(f"  {sys.executable} -m pip install pyaudio SpeechRecognition")
    print()
    print("Then run this test again.")

print("=" * 60)

