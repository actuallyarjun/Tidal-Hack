"""
SIMPLE LIVE STREAM WITH OBJECT DETECTION
All-in-one file for hackathon MVP
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# Check packages
try:
    import av
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    WEBRTC_OK = True
except ImportError:
    WEBRTC_OK = False

try:
    from ultralytics import YOLO
    YOLO_OK = True
except ImportError:
    YOLO_OK = False

# Page config
st.set_page_config(page_title="Live Navigation Assistant", layout="wide")

# Title
st.title("🔴 Live Navigation Assistant - MVP")

# Check if packages are installed
if not WEBRTC_OK:
    st.error("❌ Live stream packages not installed!")
    st.code("pip install av streamlit-webrtc")
    st.stop()

if not YOLO_OK:
    st.warning("⚠️ YOLO not installed. Showing video only.")
    st.code("pip install ultralytics")

# Initialize detector
@st.cache_resource
def load_detector():
    if YOLO_OK:
        try:
            model = YOLO("yolov8n.pt")
            return model
        except:
            return None
    return None

detector = load_detector()

# Video processor
class LiveProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        if detector is not None:
            # Run YOLO detection
            results = detector(img, conf=0.5, verbose=False)
            
            if len(results) > 0:
                result = results[0]
                boxes = result.boxes
                
                for box in boxes:
                    # Get box data
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    name = detector.names[cls]
                    
                    # Estimate distance (simple approximation)
                    height_px = abs(y2 - y1)
                    if height_px > 0:
                        distance = (1.7 * 320) / height_px  # Rough estimate
                    else:
                        distance = -1
                    
                    # Color based on distance
                    if distance < 0:
                        color = (128, 128, 128)
                    elif distance < 1.5:
                        color = (0, 0, 255)  # Red
                    elif distance < 3.0:
                        color = (0, 165, 255)  # Orange
                    else:
                        color = (0, 255, 0)  # Green
                    
                    # Draw box
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    
                    # Draw label
                    if distance > 0:
                        label = f"{name} {distance:.1f}m"
                    else:
                        label = name
                    cv2.putText(img, label, (int(x1), int(y1)-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Add status text
        cv2.putText(img, "LIVE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Video Feed")
    
    webrtc_ctx = webrtc_streamer(
        key="live-nav",
        video_processor_factory=LiveProcessor,
        rtc_configuration=RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        ),
        media_stream_constraints={"video": True, "audio": False},
    )
    
    if webrtc_ctx.state.playing:
        st.success("🟢 LIVE STREAM ACTIVE!")
    else:
        st.info("Click START above ↑")

with col2:
    st.subheader("ℹ️ Info")
    
    if detector:
        st.success("✅ Object detection ON")
        st.caption("Red = <1.5m danger")
        st.caption("Orange = 1.5-3m caution")  
        st.caption("Green = >3m safe")
    else:
        st.warning("○ Detection OFF")
        st.caption("Video only mode")
    
    st.markdown("---")
    st.caption("**For Hackathon:**")
    st.caption("- Point at objects")
    st.caption("- See real-time boxes")
    st.caption("- Colors show distance")
    st.caption("- Red = Stop!")

# Footer
st.markdown("---")
st.caption("Vision Navigation Assistant MVP - Hackathon Demo")

