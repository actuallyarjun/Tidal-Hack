"""
SIMPLE LIVE STREAM TEST
Test if webcam streaming works with minimal code
"""
import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Live Stream Test", layout="wide")

st.title("🔴 Live Stream Test")

# Test 1: Check if av is installed
st.header("1. Check Packages")
try:
    import av
    st.success(f"✅ av package installed: {av.__version__}")
except ImportError as e:
    st.error(f"❌ av package NOT found: {e}")
    st.stop()

try:
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    st.success("✅ streamlit-webrtc installed")
except ImportError as e:
    st.error(f"❌ streamlit-webrtc NOT found: {e}")
    st.stop()

# Test 2: Simple webcam test without processing
st.header("2. Basic Webcam Test")
st.info("Click START below to test your webcam")

class SimpleVideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Just add text, no detection
        cv2.putText(img, "LIVE STREAM WORKING!", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="test",
    video_processor_factory=SimpleVideoProcessor,
    rtc_configuration=RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ),
    media_stream_constraints={"video": True, "audio": False},
)

if webrtc_ctx.state.playing:
    st.success("🟢 STREAM IS ACTIVE!")
else:
    st.warning("⚪ Click START to begin")

st.markdown("---")
st.caption("If you see 'LIVE STREAM WORKING!' on your video, everything is working!")

