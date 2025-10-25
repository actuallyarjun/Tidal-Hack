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
        
        # Improved focal length estimation for common devices
        if focal_length is None:
            # Check if manual focal length provided in settings
            if settings.focal_length_mm and settings.sensor_height_mm:
                # Use manual camera specs if provided
                self.focal_length = (settings.focal_length_mm / settings.sensor_height_mm) * image_height
            else:
                # Auto-calibrate based on typical webcam/phone cameras
                # Most webcams: ~60-70 degree FOV, phones: ~70-80 degree FOV
                # For 720p: typical focal length is ~600-800 pixels
                # For 480p: typical focal length is ~400-500 pixels
                
                # Use adaptive estimation based on resolution
                if image_height >= 720:
                    # HD webcam (720p/1080p)
                    self.focal_length = image_height * 0.9  # ~650 for 720p
                elif image_height >= 480:
                    # Standard webcam (480p)
                    self.focal_length = image_height * 1.0  # ~480 for 480p
                else:
                    # Lower resolution
                    self.focal_length = image_height * 1.2
        else:
            self.focal_length = focal_length
        
        # Load calibration factor from settings
        self.calibration_factor = settings.calibration_factor
        
        print(f"Distance Estimator initialized:")
        print(f"  Image Height: {image_height}px")
        print(f"  Focal Length: {self.focal_length:.1f}px")
        print(f"  Calibration Factor: {self.calibration_factor:.2f}")
    
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
        # Apply calibration factor for real-world adjustment
        distance = (real_height * self.focal_length * self.calibration_factor) / object_height_px
        
        # Clamp to reasonable range (0.1m to 20m)
        distance = max(0.1, min(20.0, distance))
        
        return round(distance, 2)
    
    def calibrate(self, bbox: Tuple[float, float, float, float], 
                  class_name: str, known_distance: float):
        """
        Calibrate the estimator using a known object at known distance.
        
        Args:
            bbox: Bounding box of reference object
            class_name: Object class name
            known_distance: Actual measured distance in meters
        
        Example:
            # Measure a person standing 2 meters away
            estimator.calibrate(person_bbox, 'person', 2.0)
        """
        _, y1, _, y2 = bbox
        object_height_px = abs(y2 - y1)
        
        if object_height_px == 0:
            return
        
        real_height = self.OBJECT_HEIGHTS.get(class_name.lower(), 1.0)
        
        # Calculate what the focal length should be for accurate distance
        # known_distance = (real_height * focal_length * calibration) / object_height_px
        # calibration = (known_distance * object_height_px) / (real_height * focal_length)
        self.calibration_factor = (known_distance * object_height_px) / (real_height * self.focal_length)
        
        print(f"✓ Calibrated! Adjustment factor: {self.calibration_factor:.2f}")
        print(f"  Reference: {class_name} at {known_distance}m, {object_height_px:.0f}px tall")
    
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


