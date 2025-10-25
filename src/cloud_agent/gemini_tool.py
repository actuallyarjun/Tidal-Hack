"""
Gemini VLM tool for semantic scene understanding.
"""
from typing import Dict
import numpy as np
from config.settings import settings
from src.cloud_agent.mock_responses import MockResponseGenerator


class GeminiVLMTool:
    """Gemini Vision Language Model tool for scene description."""
    
    def __init__(self):
        """Initialize Gemini API client."""
        self.api_available = False
        self.model = None
        
        # Check if Gemini API key is available
        if settings.has_gemini_key() and settings.use_gemini:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.gemini_api_key)
                
                # Use Gemini 2.0 Flash Experimental for better navigation
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.api_available = True
                print("[GEMINI] Using Gemini 2.0 Flash Experimental - Latest model")
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}")
                print("Using mock responses instead.")
        else:
            print("Gemini API not configured. Using mock responses.")
        
        # System prompt for accessibility-focused descriptions
        self.system_prompt = """You are an AI assistant helping visually impaired users navigate their environment safely.

Your role is to:
1. Provide clear, concise descriptions of the scene
2. Prioritize safety-critical information (obstacles, hazards)
3. Use spatial language (left, right, ahead, behind, distance in meters)
4. Be respectful and empowering - never patronizing
5. Focus on actionable information

When describing objects, always include:
- What the object is
- Where it is located (position and distance)
- Any immediate hazards or navigation concerns

Keep responses under 3 sentences unless asked for more detail."""
    
    def generate_description(
        self, 
        image: np.ndarray, 
        structured_cv_data: Dict,
        user_query: str = "Describe what you see"
    ) -> str:
        """
        Generate semantic scene description using Gemini.
        
        Args:
            image: Image frame (numpy array, BGR format)
            structured_cv_data: Structured CV output from edge detector
            user_query: User's question or request
        
        Returns:
            Natural language description
        """
        # If Gemini not available, use mock responses
        if not self.api_available or self.model is None:
            return MockResponseGenerator.generate_description(structured_cv_data, user_query)
        
        try:
            import cv2
            from PIL import Image as PILImage
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = PILImage.fromarray(image_rgb)
            
            # Construct grounded prompt with CV data
            cv_context = self._format_cv_data(structured_cv_data)
            
            prompt = f"""{self.system_prompt}

DETECTED OBJECTS (from computer vision):
{cv_context}

USER QUERY: {user_query}

Provide a natural, conversational response that helps the user understand their environment and navigate safely."""
            
            # Generate response
            response = self.model.generate_content([prompt, pil_image])
            
            return response.text
            
        except Exception as e:
            print(f"Error in Gemini API call: {e}")
            print("Falling back to mock responses.")
            return MockResponseGenerator.generate_description(structured_cv_data, user_query)
    
    def _format_cv_data(self, cv_data: Dict) -> str:
        """Format structured CV data for prompt."""
        if not cv_data or cv_data.get('num_objects', 0) == 0:
            return "No objects detected."
        
        lines = []
        for obj in cv_data['objects']:
            distance_str = f"{obj['distance_m']:.1f} meters" if obj['distance_m'] > 0 else "unknown distance"
            lines.append(
                f"- {obj['class']} at {distance_str}, positioned to your {obj['position']}"
            )
        
        # Highlight critical alerts
        if cv_data.get('critical_alerts'):
            lines.append("\nCRITICAL ALERTS (very close objects):")
            for alert in cv_data['critical_alerts']:
                lines.append(f"⚠ {alert['class']} only {alert['distance_m']:.1f}m away!")
        
        return "\n".join(lines)
    
    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        return self.api_available

