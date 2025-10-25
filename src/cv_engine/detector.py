"""
Real-time object detection using YOLOv8.
"""
import cv2
import numpy as np
from typing import List, Dict, Tuple
import time
from config.settings import settings
from src.cv_engine.distance_estimator import DistanceEstimator


class ObjectDetector:
    """YOLOv8-based object detector with distance estimation."""
    
    def __init__(self, model_path: str = None):
        """
        Initialize object detector.
        
        Args:
            model_path: Path to YOLO model weights
        """
        model_path = model_path or settings.yolo_model_path
        print(f"Loading YOLO model from: {model_path}")
        
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.model_loaded = True
        except Exception as e:
            print(f"Warning: Could not load YOLO model: {e}")
            print("Running in mock detection mode.")
            self.model = None
            self.model_loaded = False
        
        self.confidence_threshold = settings.confidence_threshold
        self.iou_threshold = settings.iou_threshold
        self.distance_estimator = None
        
        # Performance tracking
        self.frame_count = 0
        self.total_inference_time = 0.0
    
    def detect(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Dict]]:
        """
        Perform object detection on frame.
        
        Args:
            frame: Input image frame (BGR format)
        
        Returns:
            Tuple of (annotated_frame, detections_list)
        """
        start_time = time.time()
        
        # Initialize distance estimator with frame dimensions
        if self.distance_estimator is None:
            height, width = frame.shape[:2]
            self.distance_estimator = DistanceEstimator(image_height=height)
        
        # Check if model is loaded
        if not self.model_loaded:
            # Return empty detections if model not loaded
            annotated_frame = frame.copy()
            cv2.putText(
                annotated_frame,
                "YOLO Model Not Loaded - Install dependencies",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )
            return annotated_frame, []
        
        # Run inference
        results = self.model(
            frame, 
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            verbose=False
        )
        
        # Process results
        detections = []
        annotated_frame = frame.copy()
        
        if len(results) > 0:
            result = results[0]
            boxes = result.boxes
            
            for box in boxes:
                # Extract box data
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                bbox = (float(x1), float(y1), float(x2), float(y2))
                
                # Estimate distance
                distance = self.distance_estimator.estimate_distance(bbox, class_name)
                position = self.distance_estimator.calculate_relative_position(
                    bbox, frame.shape[1]
                )
                safety_level = self.distance_estimator.get_safety_level(distance)
                
                # Store detection
                detection = {
                    'class': class_name,
                    'confidence': round(confidence, 2),
                    'bbox': bbox,
                    'distance_m': distance,
                    'position': position,
                    'safety_level': safety_level,
                    'class_id': class_id
                }
                detections.append(detection)
                
                # Draw bounding box
                color = self._get_color_for_distance(distance)
                cv2.rectangle(
                    annotated_frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    color,
                    2
                )
                
                # Draw label
                label = f"{class_name} {distance:.1f}m ({position})"
                self._draw_label(annotated_frame, label, (int(x1), int(y1) - 10), color)
        
        # Calculate latency
        inference_time = (time.time() - start_time) * 1000  # Convert to ms
        self.frame_count += 1
        self.total_inference_time += inference_time
        
        # Draw performance metrics
        avg_latency = self.total_inference_time / self.frame_count
        fps = 1000 / inference_time if inference_time > 0 else 0
        
        cv2.putText(
            annotated_frame,
            f"Latency: {inference_time:.1f}ms | FPS: {fps:.1f} | Objects: {len(detections)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )
        
        return annotated_frame, detections
    
    def _get_color_for_distance(self, distance: float) -> Tuple[int, int, int]:
        """Get color based on distance (green=far, red=close)."""
        if distance < 0:
            return (128, 128, 128)  # Gray for unknown
        elif distance < 1.0:
            return (0, 0, 255)  # Red - critical
        elif distance < 1.5:
            return (0, 69, 255)  # Orange-red - warning
        elif distance < 3.0:
            return (0, 165, 255)  # Orange - caution
        else:
            return (0, 255, 0)  # Green - safe
    
    def _draw_label(
        self, 
        frame: np.ndarray, 
        label: str, 
        position: Tuple[int, int], 
        color: Tuple[int, int, int]
    ):
        """Draw label with background."""
        (label_width, label_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        
        cv2.rectangle(
            frame,
            position,
            (position[0] + label_width, position[1] - label_height - 5),
            color,
            -1
        )
        
        cv2.putText(
            frame,
            label,
            (position[0], position[1] - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
    
    def get_structured_output(self, detections: List[Dict]) -> Dict:
        """
        Convert detections to structured JSON format for cloud agent.
        
        Args:
            detections: List of detection dictionaries
        
        Returns:
            Structured JSON payload
        """
        # Sort by distance (closest first) for safety priority
        sorted_detections = sorted(
            detections, 
            key=lambda x: x['distance_m'] if x['distance_m'] > 0 else float('inf')
        )
        
        # Find critical alerts (very close objects)
        critical_alerts = [
            d for d in sorted_detections 
            if d['distance_m'] > 0 and d['distance_m'] < 1.5
        ]
        
        # Determine overall safety status
        if len(critical_alerts) > 0:
            if any(d['distance_m'] < 1.0 for d in critical_alerts):
                safety_status = "DANGER - Immediate obstacles detected"
            else:
                safety_status = "WARNING - Close obstacles detected"
        elif len(detections) == 0:
            safety_status = "CLEAR - No obstacles detected"
        else:
            safety_status = "CAUTION - Objects present, path negotiable"
        
        return {
            'timestamp': time.time(),
            'num_objects': len(detections),
            'objects': sorted_detections,
            'critical_alerts': critical_alerts,
            'safety_status': safety_status
        }


