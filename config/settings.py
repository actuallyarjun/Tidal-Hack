"""
Configuration settings for the Vision Navigation Assistant.
Gemini-powered AI navigation system.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API (Primary AI Engine)
    gemini_api_key: str = Field(default="", description="Gemini API key")
    use_gemini: bool = Field(default=True, description="Enable Gemini VLM")
    
    # Google Maps (Optional - for future route planning)
    google_maps_api_key: Optional[str] = Field(default=None, description="Google Maps API key")
    
    # Feature Flags
    mock_mode: bool = Field(default=False, description="Use mock responses when Gemini unavailable")
    
    # CV Model Configuration
    yolo_model_path: str = Field(
        default="src/cv_engine/models/yolov8n.pt",
        description="Path to YOLO model weights"
    )
    confidence_threshold: float = Field(default=0.5, description="Detection confidence threshold")
    iou_threshold: float = Field(default=0.45, description="IOU threshold for NMS")
    
    # Performance Settings
    target_fps: int = Field(default=30, description="Target frames per second")
    max_detection_latency_ms: int = Field(default=100, description="Max detection latency in ms")
    
    # Audio Settings
    tts_rate: int = Field(default=150, description="Text-to-speech rate")
    tts_volume: float = Field(default=0.9, description="TTS volume (0.0 - 1.0)")
    use_online_tts: bool = Field(default=False, description="Use online TTS (gTTS) vs offline")
    
    # Distance Estimation
    calibration_factor: float = Field(default=1.0, description="Distance calibration adjustment factor")
    # Advanced camera calibration (optional - app auto-detects if not set)
    focal_length_mm: Optional[float] = Field(default=None, description="Camera focal length in mm")
    sensor_height_mm: Optional[float] = Field(default=None, description="Camera sensor height in mm")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
    
    def has_gemini_key(self) -> bool:
        """Check if Gemini API key is configured."""
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")
    
    def get_feature_status(self) -> dict:
        """Get status of all features."""
        return {
            "gemini_api": self.has_gemini_key(),
            "use_gemini": self.use_gemini and self.has_gemini_key(),
            "mock_mode": self.mock_mode or not self.has_gemini_key(),
        }


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"Warning: Could not load settings from .env file: {e}")
    print("Using default settings with mock mode enabled.")
    settings = Settings(mock_mode=True)

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


