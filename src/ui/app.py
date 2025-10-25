"""
Streamlit UI for Vision Navigation Assistant Demo.
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
from typing import Optional

# Import our modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.cv_engine.detector import ObjectDetector
from src.cloud_agent.local_agent import LocalNavigationAgent
from src.audio.tts_output import TTSEngine
from src.audio.speech_input import SpeechRecognizer
from config.settings import settings

# Try to import webrtc for streaming (optional)
WEBRTC_AVAILABLE = False
WEBRTC_ERROR = None
try:
    import av
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    WEBRTC_AVAILABLE = True
    print("="* 60)
    print("[OK] WebRTC packages loaded successfully!")
    print(f"[OK] av version: {av.__version__}")
    print(f"[OK] WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
    print("="* 60)
except ImportError as e:
    WEBRTC_ERROR = str(e)
    print("="* 60)
    print(f"[NO] WebRTC import failed: {e}")
    print("[NO] Install with: pip install streamlit-webrtc av")
    print(f"[NO] WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
    print("="* 60)
    WEBRTC_AVAILABLE = False
except Exception as e:
    WEBRTC_ERROR = str(e)
    print("="* 60)
    print(f"[ERR] Unexpected error: {e}")
    print(f"[ERR] WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
    print("="* 60)
    WEBRTC_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Vision Navigation Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .status-clear {
        background-color: #C8E6C9;
        color: #2E7D32;
    }
    .status-caution {
        background-color: #FFE082;
        color: #F57F17;
    }
    .status-danger {
        background-color: #FFCDD2;
        color: #C62828;
    }
    .metric-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .object-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.25rem;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


def initialize_components():
    """Initialize all system components."""
    if 'initialized' not in st.session_state:
        with st.spinner("Initializing system components..."):
            # Initialize detector
            st.session_state.detector = ObjectDetector()
            
            # Initialize Gemini-powered agent
            st.session_state.agent = LocalNavigationAgent()
            
            # Initialize TTS
            st.session_state.tts = TTSEngine()
            
            # Initialize speech recognizer
            st.session_state.speech_recognizer = SpeechRecognizer()
            
            # State variables
            st.session_state.last_detection = None
            st.session_state.conversation_log = []
            st.session_state.initialized = True


def render_header():
    """Render page header."""
    st.markdown('<div class="main-header">👁️ Vision Navigation Assistant</div>', unsafe_allow_html=True)
    st.markdown("**🔴 LIVE Real-Time AI Navigation • Powered by Gemini**")
    
    # Display feature status
    feature_status = settings.get_feature_status()
    status_icons = []
    
    if WEBRTC_AVAILABLE:
        status_icons.append("🔴 Live Stream")
    else:
        status_icons.append("⚠️ Stream Unavailable")
    
    if feature_status['use_gemini']:
        status_icons.append("✓ Gemini AI")
    else:
        status_icons.append("○ Basic Mode")
    
    st.caption(" | ".join(status_icons))
    st.markdown("---")
    
    # Announce app status via TTS on first load
    if 'announced' not in st.session_state:
        st.session_state.announced = True
        if hasattr(st.session_state, 'tts') and st.session_state.tts.is_available():
            status_message = "Vision Navigation Assistant ready."
            if WEBRTC_AVAILABLE:
                status_message += " Live stream available."
            if feature_status['use_gemini']:
                status_message += " Gemini AI active."
            st.session_state.tts.speak(status_message, blocking=False)


def render_sidebar():
    """Render sidebar with settings."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Mode selection - Live Stream is PRIMARY mode
        # Debug: Show actual status
        st.caption(f"Debug: WEBRTC_AVAILABLE = {WEBRTC_AVAILABLE}")
        
        if WEBRTC_AVAILABLE:
            mode_options = ["Live Webcam Stream", "Upload Image", "Webcam Snapshot"]
            st.success("🔴 Live Stream Ready!")
        else:
            mode_options = ["Upload Image", "Webcam Snapshot"]
            st.error("⚠️ LIVE STREAM UNAVAILABLE")
            if WEBRTC_ERROR:
                st.caption(f"Error: {WEBRTC_ERROR}")
            st.info("Install: pip install streamlit-webrtc av")
            st.caption("Then restart the app")
        
        demo_mode = st.radio(
            "Demo Mode",
            mode_options,
            index=0,  # Default to first option (Live Stream when available)
            help="Live Stream is the primary mode for real-time navigation"
        )
        
        st.markdown("---")
        st.header("📊 System Info")
        
        # Feature status
        feature_status = settings.get_feature_status()
        
        # Check actual availability
        speech_available = st.session_state.speech_recognizer.is_available() if hasattr(st.session_state, 'speech_recognizer') else False
        tts_available = st.session_state.tts.is_available() if hasattr(st.session_state, 'tts') else False
        
        st.info(f"""
        **CV Engine:** YOLOv8n  
        **AI Engine:** {"Gemini 2.0 Flash ✓" if feature_status['use_gemini'] else "Basic Mode"}  
        **TTS:** {"Enabled ✓" if tts_available else "Disabled ✗"}  
        **Speech:** {"Enabled ✓" if speech_available else "Disabled ✗"}
        """)
        
        # Show warning if speech is disabled
        if not speech_available:
            st.warning("⚠️ Voice commands unavailable")
            st.caption("Run: pip install pyaudio SpeechRecognition")
        
        st.markdown("---")
        st.subheader("Actions")
        
        if st.button("🗑️ Clear Conversation"):
            st.session_state.conversation_log = []
            st.session_state.agent.clear_history()
            st.success("Conversation cleared!")
        
        if st.button("🔄 Reset System"):
            st.session_state.last_detection = None
            st.session_state.conversation_log = []
            st.session_state.agent.clear_history()
            st.success("System reset!")
        
        st.markdown("---")
        st.caption("Vision Navigation Assistant v1.0")
        st.caption("Hackathon MVP Demo")
    
    return demo_mode


# Define VideoProcessor only if WebRTC is available
if WEBRTC_AVAILABLE:
    class VideoProcessor(VideoProcessorBase):
        """Video processor for real-time webcam detection."""
        
        def __init__(self):
            # Wait for session state to be initialized
            if 'detector' in st.session_state:
                self.detector = st.session_state.detector
            else:
                # Detector not initialized yet, initialize it now
                from src.cv_engine.detector import ObjectDetector
                self.detector = ObjectDetector()
                st.session_state.detector = self.detector
            self.frame_count = 0
        
        def recv(self, frame):  # Type hint removed for compatibility
            """Process incoming video frame."""
            import av
            # Convert to numpy array
            img = frame.to_ndarray(format="bgr24")
            
            # Run detection
            annotated_frame, detections = self.detector.detect(img)
            
            # ALWAYS store latest frame, even if no objects detected
            # User might ask "what do you see?" and we need the frame!
            structured_data = self.detector.get_structured_output(detections) if detections else {
                'objects': [],
                'total_objects': 0,
                'safety_status': 'clear',
                'nearest_distance': None
            }
            
            st.session_state.last_detection = {
                'frame': img,
                'data': structured_data,
                'timestamp': time.time()
            }
            
            self.frame_count += 1
            
            # Debug logging every 30 frames (once per second at ~30fps)
            if self.frame_count % 30 == 0:
                obj_count = structured_data.get('total_objects', 0)
                print(f"[VIDEO] Frame {self.frame_count} processed | Objects: {obj_count} | Detection saved: YES")
            
            # Convert back to av.VideoFrame
            return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
else:
    # Dummy class for when WebRTC is not available
    class VideoProcessor:
        pass


def render_video_feed(demo_mode):
    """Render video feed section."""
    st.header("📹 Image Analysis")
    
    uploaded_file = None
    webcam_image = None
    
    if demo_mode == "Live Webcam Stream":
        if WEBRTC_AVAILABLE:
            st.info("📹 **Live Stream Mode** - Real-time object detection")
            st.caption("Allow camera access when prompted by your browser")
            
            # WebRTC streamer for real-time video
            webrtc_ctx = webrtc_streamer(
                key="vision-nav-stream",
                video_processor_factory=VideoProcessor,
                rtc_configuration=RTCConfiguration(
                    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                ),
                media_stream_constraints={
                    "video": {
                        "width": {"ideal": 1280},
                        "height": {"ideal": 720},
                    },
                    "audio": False
                },
                async_processing=True,
            )
            
            # Announce stream status via TTS
            stream_status_key = f"stream_status_{webrtc_ctx.state.playing}"
            if stream_status_key not in st.session_state:
                st.session_state[stream_status_key] = True
                if hasattr(st.session_state, 'tts') and st.session_state.tts.is_available():
                    if webrtc_ctx.state.playing:
                        st.session_state.tts.speak("Live stream active. Real-time detection running.", blocking=False)
                    else:
                        st.session_state.tts.speak("Stream inactive. Click START to begin.", blocking=False)
            
            if webrtc_ctx.state.playing:
                st.success("🟢 Stream active - Real-time detection running")
            else:
                st.warning("⚪ Stream inactive - Click 'START' to begin")
        else:
            st.error("❌ Live stream mode requires additional packages")
            st.code("pip install streamlit-webrtc av")
            st.info("💡 Use 'Upload Image' or 'Webcam Snapshot' mode instead")
    
    elif demo_mode == "Upload Image":
        uploaded_file = st.file_uploader(
            "Upload an image", 
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image to analyze for obstacles and navigation"
        )
        
        if uploaded_file is not None:
            # Load and process image
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img_array
            
            # Run detection
            with st.spinner("Processing image..."):
                annotated_frame, detections = st.session_state.detector.detect(img_bgr)
                structured_data = st.session_state.detector.get_structured_output(detections)
                
                # Store detection
                st.session_state.last_detection = {
                    'frame': img_bgr,
                    'data': structured_data,
                    'timestamp': time.time()
                }
            
            # Display annotated image
            st.image(
                cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB), 
                use_column_width=True,
                caption="Detected Objects with Distance Estimation"
            )
    
    else:  # Webcam Snapshot
        st.info("📸 Click 'Capture from Webcam' to take a snapshot")
        
        # Webcam capture button
        if st.button("📸 Capture from Webcam", type="primary"):
            with st.spinner("Accessing webcam..."):
                # Capture from webcam
                cap = cv2.VideoCapture(0)
                
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    
                    if ret:
                        # Run detection
                        annotated_frame, detections = st.session_state.detector.detect(frame)
                        structured_data = st.session_state.detector.get_structured_output(detections)
                        
                        # Store detection
                        st.session_state.last_detection = {
                            'frame': frame,
                            'data': structured_data,
                            'timestamp': time.time()
                        }
                        
                        st.success("Image captured and processed!")
                    else:
                        st.error("Failed to capture image from webcam")
                else:
                    st.error("Could not access webcam. Please check permissions.")
        
        # Display last captured image if available
        if st.session_state.last_detection:
            annotated_frame = st.session_state.last_detection['frame']
            # Re-annotate with current detections
            _, detections = st.session_state.detector.detect(annotated_frame)
            annotated_with_boxes, _ = st.session_state.detector.detect(annotated_frame)
            
            st.image(
                cv2.cvtColor(annotated_with_boxes, cv2.COLOR_BGR2RGB),
                use_column_width=True,
                caption="Last Captured Image with Detections"
            )


def render_detection_status():
    """Render detection status panel."""
    st.header("🎯 Detection Status")
    
    if st.session_state.last_detection:
        data = st.session_state.last_detection['data']
        
        # Safety status
        safety = data.get('safety_status', 'UNKNOWN')
        if 'CLEAR' in safety:
            status_class = "status-clear"
        elif 'DANGER' in safety:
            status_class = "status-danger"
        else:
            status_class = "status-caution"
        
        st.markdown(
            f'<div class="status-box {status_class}">{safety}</div>', 
            unsafe_allow_html=True
        )
        
        # Metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f'<div class="metric-card"><h3>{data["num_objects"]}</h3><p>Objects</p></div>', 
                unsafe_allow_html=True
            )
        with col_b:
            critical_count = len(data.get('critical_alerts', []))
            st.markdown(
                f'<div class="metric-card"><h3>{critical_count}</h3><p>⚠️ Alerts</p></div>', 
                unsafe_allow_html=True
            )
        
        # Object list
        st.subheader("Detected Objects")
        if data['num_objects'] > 0:
            for obj in data['objects'][:10]:  # Show top 10
                dist = obj['distance_m']
                dist_str = f"{dist:.1f}m" if dist > 0 else "N/A"
                
                # Color code by distance
                if dist > 0 and dist < 1.0:
                    emoji = "🔴"
                elif dist > 0 and dist < 1.5:
                    emoji = "🟠"
                elif dist > 0 and dist < 3.0:
                    emoji = "🟡"
                else:
                    emoji = "🟢"
                
                st.markdown(
                    f'<div class="object-item">{emoji} <b>{obj["class"]}</b> - {dist_str} ({obj["position"]})</div>',
                    unsafe_allow_html=True
                )
        else:
            st.write("✓ No objects detected")
    else:
        st.info("👆 Upload or capture an image to see detection results")


def render_query_interface():
    """Render voice-first query interface for blind users."""
    st.markdown("---")
    st.header("🎤 Voice Commands")
    st.caption("This app is designed for voice interaction - Press the button and speak")
    
    # Show example commands
    with st.expander("📝 Example Commands (Click to expand)"):
        st.markdown("""
        **Safety Checks:**
        - "Is it safe?"
        - "Can I walk forward?"
        - "Any obstacles?"
        
        **Scene Description:**
        - "What do you see?"
        - "Describe what's ahead"
        - "What's around me?"
        
        **Navigation:**
        - "Where can I go?"
        - "Guide me"
        - "Which direction is clear?"
        
        **Find Objects:**
        - "Find the door"
        - "Where is the chair?"
        - "Locate the table"
        """)
    
    # Large, prominent voice button
    voice_button = st.button(
        "🎤 PRESS TO SPEAK",
        type="primary",
        use_container_width=True,
        help="Click this button and speak your command"
    )
    
    # Process query
    query_to_process = None
    
    # Voice input
    if voice_button:
        # Check if speech recognizer is available
        if not hasattr(st.session_state, 'speech_recognizer'):
            st.error("❌ Speech recognizer not initialized. Please refresh the page.")
            # Speak error
            if st.session_state.tts.is_available():
                st.session_state.tts.speak("Error: Speech recognizer not initialized. Please refresh the page.", blocking=False)
        elif not st.session_state.speech_recognizer.is_available():
            st.error("❌ Speech recognition not available")
            st.info("💡 Install: pip install pyaudio SpeechRecognition")
            # Speak error
            if st.session_state.tts.is_available():
                st.session_state.tts.speak("Error: Speech recognition not available. Please install required packages.", blocking=False)
        else:
            # Speech recognizer is available - try to listen
            st.info("🎤 LISTENING... Speak now!")
            
            # Speak prompt
            if st.session_state.tts.is_available():
                st.session_state.tts.speak("Listening", blocking=False)
            
            try:
                recognized_text = st.session_state.speech_recognizer.listen_once(timeout=5)
                if recognized_text:
                    # Show what was heard in LARGE, prominent text
                    st.markdown("---")
                    st.markdown("### 🎤 You Said:")
                    st.markdown(f"## **\"{recognized_text}\"**")
                    st.markdown("---")
                    
                    # Speak what was heard
                    if st.session_state.tts.is_available():
                        st.session_state.tts.speak(f"You said: {recognized_text}", blocking=False)
                    
                    query_to_process = recognized_text
                else:
                    st.warning("⚠️ No speech detected. Please try again.")
                    # Speak warning
                    if st.session_state.tts.is_available():
                        st.session_state.tts.speak("No speech detected. Please try again.", blocking=False)
            except Exception as e:
                st.error(f"❌ Speech recognition error: {e}")
                # Speak error
                if st.session_state.tts.is_available():
                    st.session_state.tts.speak("Error occurred. Please try again.", blocking=False)
    
    # Execute query
    if query_to_process:
        if not st.session_state.last_detection:
            # No detection available - inform user
            st.error("⚠️ No video feed available!")
            st.warning("The stream may be starting or the camera needs a moment...")
            
            # More helpful guidance
            st.info("""
            **What to do:**
            1. Make sure live stream is running (you should see video)
            2. Wait 2-3 seconds for first frame to process
            3. Make sure something is in view of the camera
            4. Then try your voice command again
            """)
            
            # Check terminal for frame processing logs
            st.caption("💡 Check the terminal window for [VIDEO] messages to confirm frames are being processed")
            
            if st.session_state.tts.is_available():
                st.session_state.tts.speak("Waiting for video feed. Make sure the stream is running.", blocking=False)
        else:
            # Speak "thinking"
            if st.session_state.tts.is_available():
                st.session_state.tts.speak("Thinking", blocking=False)
                
            with st.spinner("🤔 AI is thinking..."):
                # Get agent response
                response = st.session_state.agent.process_query(
                    query_to_process,
                    st.session_state.last_detection['frame'],
                    st.session_state.last_detection['data']
                )
            
            # Display response in LARGE, prominent text
            st.markdown("---")
            st.markdown("### 🤖 AI Response:")
            st.markdown(f"## **{response['text_response']}**")
            st.markdown("---")
            
            # Show which system was used
            if response.get('used_vlm'):
                st.caption("🌟 Using Gemini AI")
            else:
                st.caption("🔧 Using basic mode")
            
            # Speak response (MOST IMPORTANT - blind users need to hear this!)
            if st.session_state.tts.is_available():
                st.session_state.tts.speak(response['text_response'], blocking=False)
                st.success("🔊 Speaking response...")
            else:
                st.warning("⚠️ Text-to-speech not available")
            
            # Log conversation
            st.session_state.conversation_log.append({
                'query': query_to_process,
                'response': response['text_response'],
                'timestamp': time.time()
            })
            
            # Show haptic feedback if enabled
            if response['haptic_feedback'].get('enabled'):
                haptic = response['haptic_feedback']
                st.warning(
                    f"⚠️ **Haptic Alert:** {haptic['pattern'].replace('_', ' ').title()} "
                    f"({haptic['direction']}, intensity: {haptic['intensity']:.0%})"
                )
    
    elif query_to_process and not st.session_state.last_detection:
        st.warning("Please upload or capture an image first before asking questions.")


def render_conversation_history():
    """Render conversation history."""
    if st.session_state.conversation_log:
        st.markdown("---")
        st.header("📜 Conversation History")
        
        # Show recent conversations (last 5)
        for i, exchange in enumerate(reversed(st.session_state.conversation_log[-5:])):
            with st.expander(
                f"💬 Exchange {len(st.session_state.conversation_log) - i}",
                expanded=(i == 0)
            ):
                st.markdown(f"**You:** {exchange['query']}")
                st.markdown(f"**AI:** {exchange['response']}")
                st.caption(f"Time: {time.strftime('%H:%M:%S', time.localtime(exchange['timestamp']))}")


def main():
    """Main application."""
    # Initialize components FIRST before anything else
    initialize_components()
    
    # Verify initialization completed
    if 'initialized' not in st.session_state:
        st.error("Failed to initialize components. Please refresh the page.")
        st.stop()
    
    # Render header
    render_header()
    
    # Render sidebar and get mode
    demo_mode = render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_video_feed(demo_mode)
    
    with col2:
        render_detection_status()
    
    # Query interface
    render_query_interface()
    
    # Conversation history
    render_conversation_history()


if __name__ == "__main__":
    main()

