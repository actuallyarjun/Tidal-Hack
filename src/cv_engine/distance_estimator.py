"""
Monocular distance estimation using object detection and camera calibration.
"""
import numpy as np
from typing import Dict, Tuple
from config.settings import settings


class DistanceEstimator:
    """
    Estimates distance to objects using monocular vision.
    Uses simple pinhole camera model for MVP.
    """
    
    # Average real-world object heights (meters)
    OBJECT_HEIGHTS = {
        'person': 1.7,
        'car': 1.5,
        'chair': 0.9,
        'bottle': 0.25,
        'cup': 0.12,
        'laptop': 0.02,
        'cell phone': 0.15,
        'door': 2.0,
        'bicycle': 1.1,
        'dog': 0.6,
        'cat': 0.25,
        'couch': 0.8,
        'table': 0.75,
        'bed': 0.6,
        'tv': 0.5,
        'potted plant': 0.5,
        'backpack': 0.5,
        'handbag': 0.3,
        'suitcase': 0.7,
        'book': 0.25,
        'clock': 0.3,
        'vase': 0.3,
        'scissors': 0.2,
        'teddy bear': 0.3,
        'hair drier': 0.25,
        'toothbrush': 0.2,
    }
    
    def __init__(self, image_height: int = 480, focal_length: float = None):
        """
        Initialize distance estimator.
        
        Args:
            image_height: Camera image height in pixels
            focal_length: Camera focal length in pixels (calibrated)
        """
        self.image_height = image_height
        
        # Approximate focal length calculation if not provided
        if focal_length is None:
            # Typical smartphone: focal_length_px = (focal_length_mm / sensor_height_mm) * image_height_px
            self.focal_length = (settings.focal_length_mm / settings.sensor_height_mm) * image_height
        else:
            self.focal_length = focal_length
    
    def estimate_distance(
        self, 
        bbox: Tuple[float, float, float, float], 
        class_name: str
    ) -> float:
        """
        Estimate distance to object using pinhole camera model.
        
        Args:
            bbox: Bounding box (x1, y1, x2, y2) in pixels
            class_name: Detected object class
        
        Returns:
            Estimated distance in meters
        """
        # Get object height in pixels
        _, y1, _, y2 = bbox
        object_height_px = abs(y2 - y1)
        
        if object_height_px == 0:
            return -1.0  # Invalid
        
        # Get real-world object height
        real_height = self.OBJECT_HEIGHTS.get(class_name.lower(), 1.0)
        
        # Distance = (Real Height × Focal Length) / Pixel Height
        distance = (real_height * self.focal_length) / object_height_px
        
        return round(distance, 2)
    
    def calculate_relative_position(
        self, 
        bbox: Tuple[float, float, float, float], 
        image_width: int
    ) -> str:
        """
        Calculate relative horizontal position of object.
        
        Args:
            bbox: Bounding box (x1, y1, x2, y2)
            image_width: Image width in pixels
        
        Returns:
            Position description: 'left', 'center', 'right'
        """
        x1, _, x2, _ = bbox
        center_x = (x1 + x2) / 2
        
        # Divide image into thirds
        if center_x < image_width / 3:
            return "left"
        elif center_x > 2 * image_width / 3:
            return "right"
        else:
            return "center"
    
    def get_safety_level(self, distance: float) -> str:
        """
        Get safety level based on distance.
        
        Args:
            distance: Distance in meters
        
        Returns:
            Safety level: 'critical', 'warning', 'caution', 'safe'
        """
        if distance < 0:
            return "unknown"
        elif distance < 1.0:
            return "critical"
        elif distance < 1.5:
            return "warning"
        elif distance < 3.0:
            return "caution"
        else:
            return "safe"


