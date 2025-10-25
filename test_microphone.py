"""
Quick Microphone Test
Run this to test if your microphone is working before using the full app
"""

import sys

print("="*60)
print("         MICROPHONE TEST")
print("="*60)
print()

# Test 1: Check packages
print("TEST 1: Checking required packages...")
try:
    import speech_recognition as sr
    print("[OK] speech_recognition installed")
except ImportError:
    print("[FAIL] speech_recognition NOT installed")
    print("       Run: pip install SpeechRecognition")
    sys.exit(1)

try:
    import pyaudio
    print("[OK] pyaudio installed")
except ImportError:
    print("[FAIL] pyaudio NOT installed")
    print("       Run: pip install pyaudio")
    sys.exit(1)

print()

# Test 2: List microphones
print("TEST 2: Detecting microphones...")
try:
    mics = sr.Microphone.list_microphone_names()
    print(f"[OK] Found {len(mics)} microphone(s):")
    for i, name in enumerate(mics):
        print(f"     {i}: {name}")
except Exception as e:
    print(f"[FAIL] Could not list microphones: {e}")
    sys.exit(1)

print()

# Test 3: Initialize recognizer
print("TEST 3: Initializing speech recognizer...")
try:
    recognizer = sr.Recognizer()
    
    # ULTRA-SENSITIVE settings
    recognizer.energy_threshold = 100
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.4
    
    microphone = sr.Microphone()
    print("[OK] Recognizer initialized")
    print(f"     Energy threshold: {recognizer.energy_threshold}")
    print(f"     Pause threshold: {recognizer.pause_threshold}s")
except Exception as e:
    print(f"[FAIL] Could not initialize: {e}")
    sys.exit(1)

print()

# Test 4: Quick calibration
print("TEST 4: Calibrating to ambient noise...")
print("        (Please be QUIET for 1 second)")
try:
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
    print(f"[OK] Calibrated! New energy threshold: {recognizer.energy_threshold}")
except Exception as e:
    print(f"[FAIL] Calibration failed: {e}")
    sys.exit(1)

print()

# Test 5: Actual recording test
print("TEST 5: Recording audio...")
print()
print("="*60)
print("    🎤 SAY SOMETHING NOW - LOUD and CLEAR!")
print("       Try: 'What do you see?'")
print("       You have 3 seconds...")
print("="*60)
print()

try:
    with microphone as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
    print("[OK] Audio captured successfully!")
    print(f"     Audio duration: {len(audio.get_raw_data())/32000:.1f} seconds")
except sr.WaitTimeoutError:
    print("[FAIL] No audio detected (timeout)")
    print("       Possible issues:")
    print("       - Microphone not working")
    print("       - Energy threshold too high")
    print("       - You're too quiet")
    print("       - Wrong microphone selected")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] Recording error: {e}")
    sys.exit(1)

print()

# Test 6: Speech recognition
print("TEST 6: Recognizing speech with Google API...")
print("        (This requires internet connection)")
try:
    text = recognizer.recognize_google(audio)
    print()
    print("="*60)
    print("         ✓✓✓ SUCCESS! ✓✓✓")
    print("="*60)
    print(f"You said: '{text}'")
    print("="*60)
    print()
    print("[OK] Your microphone is working perfectly!")
    print()
except sr.UnknownValueError:
    print("[WARN] Google could not understand audio")
    print("       Audio was captured but not clear enough")
    print("       Try speaking LOUDER and CLEARER")
except sr.RequestError as e:
    print(f"[FAIL] Google API error: {e}")
    print("       Check your internet connection")
except Exception as e:
    print(f"[FAIL] Recognition error: {e}")

print()
print("="*60)
print("         TEST COMPLETE")
print("="*60)
print()
print("If all tests passed, your microphone works!")
print("If any failed, check the error messages above.")
print()

