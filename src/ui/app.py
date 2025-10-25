"""
Streamlit UI for Vision Navigation Assistant Demo.
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
from typing import Optional
import av

# Import our modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.cv_engine.detector import ObjectDetector
from src.cloud_agent.local_agent import LocalNavigationAgent
from src.cloud_agent.bedrock_agent import BedrockNavigationAgent
from src.audio.tts_output import TTSEngine
from src.audio.speech_input import SpeechRecognizer
from config.settings import settings

# Import webrtc for streaming
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

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
            
            # Initialize agent (use Bedrock if configured, otherwise local)
            if settings.use_bedrock and settings.has_bedrock_agent():
                st.session_state.agent = BedrockNavigationAgent()
            else:
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
    st.markdown("**AI-Powered Real-Time Navigation for the Visually Impaired**")
    
    # Display feature status
    feature_status = settings.get_feature_status()
    status_icons = []
    
    if feature_status['use_gemini']:
        status_icons.append("✓ Gemini VLM")
    else:
        status_icons.append("○ Mock Responses")
    
    if feature_status['use_bedrock']:
        status_icons.append("✓ AWS Bedrock")
    else:
        status_icons.append("○ Local Agent")
    
    st.caption(" | ".join(status_icons))
    st.markdown("---")


def render_sidebar():
    """Render sidebar with settings."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Mode selection
        demo_mode = st.radio(
            "Demo Mode",
            ["Live Webcam Stream", "Upload Image", "Webcam Snapshot"],
            help="Select how to capture images for analysis"
        )
        
        st.markdown("---")
        st.header("📊 System Info")
        
        # Feature status
        feature_status = settings.get_feature_status()
        
        st.info(f"""
        **CV Engine:** YOLOv8n  
        **VLM:** {"Gemini 1.5 Pro ✓" if feature_status['use_gemini'] else "Mock Mode"}  
        **Agent:** {"AWS Bedrock ✓" if feature_status['use_bedrock'] else "Local"}  
        **TTS:** {"Enabled ✓" if st.session_state.tts.is_available() else "Disabled"}  
        **Speech:** {"Enabled ✓" if st.session_state.speech_recognizer.is_available() else "Disabled"}
        """)
        
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


class VideoProcessor(VideoProcessorBase):
    """Video processor for real-time webcam detection."""
    
    def __init__(self):
        self.detector = st.session_state.detector
        self.frame_count = 0
    
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """Process incoming video frame."""
        # Convert to numpy array
        img = frame.to_ndarray(format="bgr24")
        
        # Run detection
        annotated_frame, detections = self.detector.detect(img)
        
        # Store latest detection in session state
        if detections:
            structured_data = self.detector.get_structured_output(detections)
            st.session_state.last_detection = {
                'frame': img,
                'data': structured_data,
                'timestamp': time.time()
            }
        
        self.frame_count += 1
        
        # Convert back to av.VideoFrame
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


def render_video_feed(demo_mode):
    """Render video feed section."""
    st.header("📹 Image Analysis")
    
    uploaded_file = None
    webcam_image = None
    
    if demo_mode == "Live Webcam Stream":
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
        
        if webrtc_ctx.state.playing:
            st.success("🟢 Stream active - Real-time detection running")
        else:
            st.warning("⚪ Stream inactive - Click 'START' to begin")
    
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
    """Render query interface."""
    st.markdown("---")
    st.header("💬 Ask the AI Assistant")
    
    # Query input
    col_query, col_voice = st.columns([4, 1])
    
    with col_query:
        user_query = st.text_input(
            "Type your question",
            placeholder="e.g., 'Describe what you see' or 'Is it safe to walk forward?'",
            key="query_input"
        )
    
    with col_voice:
        st.write("")  # Spacing
        voice_button = st.button("🎤 Voice", help="Use voice input")
    
    # Process query
    query_to_process = None
    
    col_send, col_clear = st.columns([1, 1])
    
    with col_send:
        if st.button("🚀 Send Query", type="primary", use_container_width=True) and user_query:
            query_to_process = user_query
    
    with col_clear:
        if st.button("🔄 Clear Input", use_container_width=True):
            st.session_state.query_input = ""
            st.rerun()
    
    # Voice input
    if voice_button:
        if st.session_state.speech_recognizer.is_available():
            with st.spinner("🎤 Listening..."):
                recognized_text = st.session_state.speech_recognizer.listen_once(timeout=5)
                if recognized_text:
                    st.success(f"Heard: {recognized_text}")
                    query_to_process = recognized_text
                else:
                    st.warning("No speech detected. Please try again.")
        else:
            st.error("Speech recognition not available. Please install required packages.")
    
    # Execute query
    if query_to_process and st.session_state.last_detection:
        with st.spinner("🤔 AI is thinking..."):
            # Get agent response
            response = st.session_state.agent.process_query(
                query_to_process,
                st.session_state.last_detection['frame'],
                st.session_state.last_detection['data']
            )
            
            # Display response
            st.success("**AI Response:**")
            st.write(response['text_response'])
            
            # Show which system was used
            if response.get('used_vlm'):
                st.caption("🌟 Response generated using Gemini VLM")
            elif response.get('used_bedrock'):
                st.caption("☁️ Response generated using AWS Bedrock")
            else:
                st.caption("🔧 Response generated using local rules")
            
            # Speak response
            if st.session_state.tts.is_available():
                st.session_state.tts.speak(response['text_response'], blocking=False)
            
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
    # Initialize components
    initialize_components()
    
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

