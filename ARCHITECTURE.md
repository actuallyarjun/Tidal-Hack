# 🏗️ Architecture Documentation

## System Overview

The Vision Navigation Assistant implements a **modular, hybrid edge-cloud architecture** designed for:

1. **Low-latency safety-critical processing** on edge devices
2. **Enhanced semantic understanding** via cloud services
3. **Graceful degradation** when cloud services unavailable
4. **Easy transition** from MVP to production deployment

---

## Architecture Principles

### 1. Edge-First Processing

**Critical safety functions run locally:**
- Object detection (<100ms latency)
- Distance estimation
- Immediate hazard alerts
- Haptic feedback generation

**Rationale:** Navigation safety cannot depend on network latency or cloud availability.

### 2. Modular Component Design

**Each module is independently:**
- Testable
- Replaceable
- Configurable

**Benefits:**
- Swap local ↔ cloud implementations
- Add new features without refactoring
- Easy unit testing

### 3. Graceful Degradation

**System operates at multiple capability levels:**

```
Level 3: Full Cloud (Bedrock + Gemini)
  ↓ Fallback
Level 2: Local + Gemini VLM
  ↓ Fallback
Level 1: Local + Rule-based (Always works)
```

---

## Component Architecture

### 1. Computer Vision Engine (`src/cv_engine/`)

**Purpose:** Real-time object detection and distance estimation

**Components:**

```python
ObjectDetector (detector.py)
├── YOLOv8 Model
├── Distance Estimator
└── Performance Tracker

DistanceEstimator (distance_estimator.py)
├── Pinhole Camera Model
├── Object Height Database
└── Position Calculator
```

**Key Features:**
- YOLOv8n for real-time detection (30 FPS target)
- Monocular depth estimation using known object sizes
- Safety-level classification (critical/warning/caution/safe)
- Structured JSON output for agent consumption

**Output Format:**
```python
{
    'timestamp': float,
    'num_objects': int,
    'objects': [
        {
            'class': str,
            'confidence': float,
            'bbox': tuple,
            'distance_m': float,
            'position': 'left'|'center'|'right',
            'safety_level': str
        }
    ],
    'critical_alerts': [...],
    'safety_status': str
}
```

---

### 2. Cloud Agent Orchestration (`src/cloud_agent/`)

**Purpose:** Intelligent decision-making and response generation

**Architecture Pattern:** Strategy Pattern with Interface

```python
AgentInterface (agent_interface.py)
    ↑ implements
    ├── LocalNavigationAgent (local_agent.py)
    └── BedrockNavigationAgent (bedrock_agent.py)
```

#### 2.1 Agent Interface

**Abstract base class ensuring:**
- Consistent API across implementations
- Easy swapping of agent types
- Standard conversation management

**Core Methods:**
```python
process_query(user_query, image_frame, cv_data) -> response
get_conversation_history() -> List[Dict]
clear_history() -> None
```

#### 2.2 Local Navigation Agent

**Orchestrates:**
1. CV data processing
2. Safety alert checking
3. VLM decision logic
4. Response generation

**Decision Tree:**
```
User Query
    ↓
Needs VLM? ──Yes──→ Gemini Available? ──Yes──→ Gemini Response
    ↓ No                    ↓ No
    └──────────────────────→ Rule-based Response
```

**Features:**
- Conversation history (last 5 exchanges)
- Intelligent VLM routing (saves API calls)
- Tool invocation (haptic, localization)
- CV data summarization

#### 2.3 Bedrock Navigation Agent

**AWS Integration:**
- boto3 client for Bedrock Agent Runtime
- Streaming response handling
- Session management
- Automatic fallback to local agent

**Configuration Check:**
```python
if (has_aws_credentials() and 
    has_bedrock_agent() and 
    use_bedrock == True):
    # Use Bedrock
else:
    # Use Local Agent
```

#### 2.4 Gemini VLM Tool

**Purpose:** Semantic scene understanding

**Integration:**
- Gemini 1.5 Pro model
- Grounded prompts with CV data
- Accessibility-focused system prompt
- Automatic fallback to mock responses

**Prompt Engineering:**
```
System Prompt (Safety-focused)
    +
CV Data (Structured grounding)
    +
User Query (Natural language)
    ↓
Gemini 1.5 Pro
    ↓
Natural Response
```

#### 2.5 Navigation Tools

**Tool Collection:**
- `cv_perception_tool()` - Validates and enriches CV data
- `haptic_feedback_tool()` - Generates proximity-based haptic patterns
- `localization_tool()` - GPS/VIO integration point (placeholder)
- `route_planning_tool()` - Google Maps integration point (placeholder)

#### 2.6 Mock Response Generator

**Fallback System:**
- Rule-based responses from CV data
- Pattern matching on user queries
- Safety assessments
- Position-based descriptions

**Query Categories:**
1. Safety checks → "Is it safe?"
2. Scene descriptions → "Describe what you see"
3. Object locations → "Where is the chair?"
4. General → Brief summary

---

### 3. Audio I/O Module (`src/audio/`)

#### 3.1 Text-to-Speech (`tts_output.py`)

**Dual Mode:**
- **Offline (default):** pyttsx3 for instant responses
- **Online:** gTTS for better quality

**Features:**
- Async/non-blocking speech
- Voice selection (prefer female)
- Configurable rate and volume
- Thread-safe operation

#### 3.2 Speech Recognition (`speech_input.py`)

**Capabilities:**
- Single command listening
- Continuous background listening
- Ambient noise calibration
- Google Speech Recognition API

**Error Handling:**
- Timeout management
- Unknown value handling
- Service error fallback

---

### 4. User Interface (`src/ui/`)

**Framework:** Streamlit (web-based)

**UI Components:**

```
┌─────────────────────────────────────────┐
│           Header + Status Icons          │
├──────────────────┬──────────────────────┤
│                  │                      │
│  Video/Image     │  Detection Status    │
│  Feed Panel      │  - Safety Status     │
│                  │  - Object Count      │
│                  │  - Critical Alerts   │
│                  │  - Object List       │
├──────────────────┴──────────────────────┤
│         Query Interface                  │
│  [Text Input] [Voice Button]            │
├──────────────────────────────────────────┤
│         AI Response Display              │
├──────────────────────────────────────────┤
│      Conversation History                │
└──────────────────────────────────────────┘
```

**Session State Management:**
```python
st.session_state.detector        # ObjectDetector instance
st.session_state.agent           # Agent instance
st.session_state.tts             # TTS engine
st.session_state.speech_recognizer
st.session_state.last_detection  # Latest CV results
st.session_state.conversation_log
```

**Demo Modes:**
1. **Upload Image** - File upload for analysis
2. **Webcam Snapshot** - Real-time camera capture

---

## Data Flow

### End-to-End Processing Pipeline

```
┌─────────────────────────────────────────────────────────┐
│ 1. INPUT                                                 │
│    Camera/Image File                                     │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 2. EDGE PROCESSING (Local, <100ms)                      │
│    ┌──────────────────┐                                 │
│    │ YOLOv8 Detection │ → Bounding Boxes                │
│    └──────────────────┘                                 │
│    ┌──────────────────┐                                 │
│    │ Distance         │ → Depth Estimates               │
│    │ Estimation       │                                 │
│    └──────────────────┘                                 │
│    ┌──────────────────┐                                 │
│    │ Structured JSON  │ → Agent Input                   │
│    └──────────────────┘                                 │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 3. SAFETY CHECK (Immediate)                             │
│    Critical Distance? → Haptic Alert                    │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 4. AGENT PROCESSING                                      │
│    ┌──────────────────┐                                 │
│    │ Query Analysis   │ → VLM needed?                   │
│    └──────────────────┘                                 │
│    ┌──────────────────┐                                 │
│    │ Response         │ → Local or Cloud                │
│    │ Generation       │                                 │
│    └──────────────────┘                                 │
└────────────────┬────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│ 5. OUTPUT                                                │
│    ├─ Text Response (UI)                                │
│    ├─ Audio Output (TTS)                                │
│    ├─ Haptic Feedback (Virtual)                         │
│    └─ Visual Overlay (Bounding Boxes)                   │
└─────────────────────────────────────────────────────────┘
```

---

## Configuration System

**Centralized Settings:** `config/settings.py`

**Pydantic-based Configuration:**
```python
class Settings(BaseSettings):
    # AWS
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    
    # Feature Flags
    use_bedrock: bool
    use_gemini: bool
    mock_mode: bool
    
    # CV Parameters
    confidence_threshold: float
    iou_threshold: float
    
    # Audio
    tts_rate: int
    tts_volume: float
    
    # Distance Estimation
    focal_length_mm: float
    sensor_height_mm: float
```

**Environment Variables:**
- Load from `.env` file
- Fallback to defaults
- Validation on load

---

## Scaling Path: MVP → Production

### Current MVP Architecture

```
┌──────────────────┐
│  Local Machine   │
│  - Streamlit UI  │
│  - Local Agent   │
│  - CV Engine     │
└──────────────────┘
```

### Production Architecture

```
┌──────────────────┐
│  Mobile App      │
│  (React Native)  │
│  - TFLite Model  │
│  - Local CV      │
└────────┬─────────┘
         │ HTTPS
         ↓
┌──────────────────────────────────────┐
│        AWS Infrastructure             │
│  ┌────────────────────────────────┐  │
│  │     API Gateway                │  │
│  └──────────┬─────────────────────┘  │
│             ↓                         │
│  ┌────────────────────────────────┐  │
│  │  Lambda Functions (Tools)      │  │
│  │  - Navigation                  │  │
│  │  - Localization                │  │
│  │  - Route Planning              │  │
│  └──────────┬─────────────────────┘  │
│             ↓                         │
│  ┌────────────────────────────────┐  │
│  │  Bedrock Agent                 │  │
│  │  - Orchestration               │  │
│  │  - Gemini Integration          │  │
│  └──────────┬─────────────────────┘  │
│             ↓                         │
│  ┌────────────────────────────────┐  │
│  │  DynamoDB                      │  │
│  │  - User Sessions               │  │
│  │  - Object Memory               │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

### Migration Steps

1. **Phase 1: Containerize CV Engine**
   - Docker container for CV service
   - Deploy to ECS/Lambda

2. **Phase 2: Deploy Bedrock Agent**
   - Create Lambda functions for tools
   - Configure Bedrock Agent
   - Connect to knowledge bases

3. **Phase 3: Mobile App**
   - Convert YOLO to TFLite
   - Build React Native app
   - Integrate device sensors (GPS, IMU, haptics)

4. **Phase 4: Enhanced Features**
   - VIO for indoor localization
   - Google Maps integration
   - Persistent object memory (DynamoDB)
   - Real-time route guidance

---

## Performance Considerations

### Latency Budget

```
Total Target: <100ms for safety-critical path

Breakdown:
├─ Image Capture:      5-10ms
├─ YOLOv8 Inference:   30-50ms
├─ Distance Calc:      1-2ms
├─ Safety Check:       1ms
└─ Haptic Signal:      5ms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Total:              42-68ms ✓
```

### Non-Critical Path (Can be slower)

```
VLM Query: 1-3 seconds acceptable
├─ User expects thoughtful response
├─ Not safety-critical
└─ Audio output masks latency
```

### Optimization Strategies

1. **Model Selection**
   - YOLOv8n (nano) for speed
   - Upgrade to YOLOv8s if accuracy needed

2. **Caching**
   - Cache Gemini responses for similar queries
   - Reuse recent CV detections (<100ms old)

3. **Async Processing**
   - TTS runs in background thread
   - VLM calls non-blocking

4. **Batch Processing**
   - Group multiple objects in single VLM query
   - Aggregate feedback for multiple alerts

---

## Security Considerations

### Current MVP

- API keys in `.env` (git-ignored)
- No user authentication
- Local processing only

### Production Requirements

1. **Authentication & Authorization**
   - AWS Cognito for user management
   - API Gateway authentication

2. **Data Privacy**
   - Images processed locally, not stored
   - User sessions encrypted
   - HIPAA/GDPR compliance path

3. **API Key Management**
   - AWS Secrets Manager
   - Rotate credentials regularly
   - Least privilege access

---

## Testing Strategy

### Unit Tests
```python
# CV Engine
test_distance_estimation()
test_object_detection()
test_safety_classification()

# Agent
test_query_routing()
test_vlm_fallback()
test_tool_invocation()

# Audio
test_tts_output()
test_speech_recognition()
```

### Integration Tests
```python
# End-to-end
test_image_to_response()
test_safety_alert_flow()
test_conversation_context()
```

### Performance Tests
```python
test_detection_latency()
test_fps_target()
test_concurrent_users()
```

---

## Future Enhancements

### Short-term (3-6 months)
- [ ] Mobile app prototype
- [ ] TFLite model conversion
- [ ] Real haptic device integration
- [ ] Indoor localization (VIO)

### Medium-term (6-12 months)
- [ ] Google Maps integration
- [ ] Route planning and guidance
- [ ] Multi-user support
- [ ] Cloud deployment

### Long-term (12+ months)
- [ ] Stereo vision for accuracy
- [ ] Semantic SLAM
- [ ] Crowdsourced object database
- [ ] Multi-language support

---

## Conclusion

This architecture provides:

✅ **Hackathon-ready MVP** - Works without cloud setup  
✅ **Production scalability** - Clear migration path  
✅ **Safety-first design** - Edge processing for critical functions  
✅ **Modular flexibility** - Easy to extend and customize  

**The system gracefully scales from laptop demo to production deployment.**

