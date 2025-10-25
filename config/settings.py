"""
Configuration settings for the Vision Navigation Assistant.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # AWS Configuration
    aws_access_key_id: str = Field(default="", description="AWS access key ID")
    aws_secret_access_key: str = Field(default="", description="AWS secret access key")
    aws_region: str = Field(default="us-east-1", description="AWS region")
    
    # Bedrock Agent
    bedrock_agent_id: Optional[str] = Field(default=None, description="Bedrock agent ID")
    bedrock_agent_alias_id: Optional[str] = Field(default=None, description="Bedrock agent alias ID")
    
    # Gemini API
    gemini_api_key: str = Field(default="", description="Gemini API key")
    
    # Google Maps
    google_maps_api_key: Optional[str] = Field(default=None, description="Google Maps API key")
    
    # Feature Flags
    use_bedrock: bool = Field(default=False, description="Enable AWS Bedrock integration")
    use_gemini: bool = Field(default=False, description="Enable Gemini VLM")
    mock_mode: bool = Field(default=True, description="Use mock responses when APIs unavailable")
    
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
    
    # Distance Estimation (Monocular - approximate)
    focal_length_mm: float = Field(default=4.0, description="Camera focal length in mm")
    sensor_height_mm: float = Field(default=6.0, description="Camera sensor height in mm")
    avg_person_height_m: float = Field(default=1.7, description="Average person height in meters")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
    
    def has_aws_credentials(self) -> bool:
        """Check if AWS credentials are configured."""
        return bool(self.aws_access_key_id and self.aws_secret_access_key)
    
    def has_gemini_key(self) -> bool:
        """Check if Gemini API key is configured."""
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")
    
    def has_bedrock_agent(self) -> bool:
        """Check if Bedrock agent is configured."""
        return bool(self.bedrock_agent_id and self.bedrock_agent_alias_id)
    
    def get_feature_status(self) -> dict:
        """Get status of all features."""
        return {
            "aws_credentials": self.has_aws_credentials(),
            "gemini_api": self.has_gemini_key(),
            "bedrock_agent": self.has_bedrock_agent(),
            "use_bedrock": self.use_bedrock and self.has_bedrock_agent(),
            "use_gemini": self.use_gemini and self.has_gemini_key(),
            "mock_mode": self.mock_mode,
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


