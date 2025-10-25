"""
DIAGNOSTIC: Figure out what's wrong
"""
import sys
import subprocess

print("=" * 60)
print("DIAGNOSTIC REPORT")
print("=" * 60)

# 1. Which Python?
print(f"\n1. Python Executable: {sys.executable}")
print(f"   Python Version: {sys.version}")

# 2. Check av
print("\n2. Checking 'av' package:")
try:
    import av
    print(f"   [OK] av is installed: {av.__version__}")
    av_ok = True
except ImportError as e:
    print(f"   [NO] av NOT found: {e}")
    av_ok = False

# 3. Check streamlit-webrtc
print("\n3. Checking 'streamlit-webrtc' package:")
try:
    import streamlit_webrtc
    print(f"   [OK] streamlit-webrtc is installed")
    webrtc_ok = True
except ImportError as e:
    print(f"   [NO] streamlit-webrtc NOT found: {e}")
    webrtc_ok = False

# 4. Check streamlit
print("\n4. Checking 'streamlit' package:")
try:
    import streamlit
    print(f"   [OK] streamlit is installed: {streamlit.__version__}")
except ImportError as e:
    print(f"   [NO] streamlit NOT found: {e}")

# 5. Where is streamlit command?
print("\n5. Finding streamlit command:")
try:
    result = subprocess.run(["where", "streamlit"], capture_output=True, text=True, shell=True)
    print(f"   Streamlit location: {result.stdout.strip()}")
except:
    print("   Could not find streamlit command")

print("\n" + "=" * 60)
print("SOLUTION:")
print("=" * 60)

if av_ok and webrtc_ok:
    print("\n[OK] ALL PACKAGES FOUND!")
    print("\nRun this command:")
    print(f'   {sys.executable} -m streamlit run test_livestream.py')
    print("\nOr just double-click: TEST_THIS_FIRST.bat")
else:
    print("\n[NO] PACKAGES MISSING!")
    print("\nRun this command:")
    print(f'   {sys.executable} -m pip install av streamlit-webrtc')

print("=" * 60)

