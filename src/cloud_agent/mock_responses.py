"""
Mock responses for when cloud APIs are unavailable.
Provides fallback rule-based responses.
"""
from typing import Dict, List
import random


class MockResponseGenerator:
    """Generate mock responses based on CV data and query patterns."""
    
    @staticmethod
    def generate_description(cv_data: Dict, user_query: str = "") -> str:
        """
        Generate a mock description based on CV data.
        
        Args:
            cv_data: Structured CV detection data
            user_query: User's query
        
        Returns:
            Generated description text
        """
        num_objects = cv_data.get('num_objects', 0)
        objects = cv_data.get('objects', [])
        safety_status = cv_data.get('safety_status', 'UNKNOWN')
        
        # Check query type
        query_lower = user_query.lower()
        
        # Safety check queries
        if any(word in query_lower for word in ['safe', 'clear', 'walk', 'move']):
            return MockResponseGenerator._safety_response(cv_data)
        
        # Description queries
        if any(word in query_lower for word in ['describe', 'what', 'see', 'scene']):
            return MockResponseGenerator._scene_description(cv_data)
        
        # Object location queries
        if any(word in query_lower for word in ['where', 'find', 'locate']):
            return MockResponseGenerator._location_response(cv_data, user_query)
        
        # Default: brief summary
        return MockResponseGenerator._brief_summary(cv_data)
    
    @staticmethod
    def _safety_response(cv_data: Dict) -> str:
        """Generate safety assessment response."""
        critical_alerts = cv_data.get('critical_alerts', [])
        num_objects = cv_data.get('num_objects', 0)
        
        if len(critical_alerts) > 0:
            closest = critical_alerts[0]
            return (
                f"Caution! There is a {closest['class']} only {closest['distance_m']:.1f} meters away "
                f"on your {closest['position']}. Please move carefully."
            )
        elif num_objects == 0:
            return "The path ahead appears clear. No obstacles detected within range."
        else:
            objects = cv_data.get('objects', [])
            closest = objects[0] if objects else None
            if closest:
                return (
                    f"The path is generally clear. The nearest object is a {closest['class']} "
                    f"about {closest['distance_m']:.1f} meters away on your {closest['position']}."
                )
            return "The area looks navigable with some objects present."
    
    @staticmethod
    def _scene_description(cv_data: Dict) -> str:
        """Generate scene description."""
        num_objects = cv_data.get('num_objects', 0)
        objects = cv_data.get('objects', [])
        
        if num_objects == 0:
            return "I don't see any objects in the current view. The area appears open."
        
        # Group objects by position
        left_objects = [o for o in objects if o['position'] == 'left']
        center_objects = [o for o in objects if o['position'] == 'center']
        right_objects = [o for o in objects if o['position'] == 'right']
        
        parts = []
        
        if center_objects:
            obj = center_objects[0]
            parts.append(
                f"Directly ahead, there's a {obj['class']} at {obj['distance_m']:.1f} meters"
            )
        
        if left_objects:
            obj = left_objects[0]
            parts.append(
                f"on your left, a {obj['class']} at {obj['distance_m']:.1f} meters"
            )
        
        if right_objects:
            obj = right_objects[0]
            parts.append(
                f"on your right, a {obj['class']} at {obj['distance_m']:.1f} meters"
            )
        
        if not parts:
            obj = objects[0]
            parts.append(
                f"I see a {obj['class']} at {obj['distance_m']:.1f} meters to your {obj['position']}"
            )
        
        description = "I can see: " + ", ".join(parts) + "."
        
        if num_objects > 3:
            description += f" There are {num_objects - 3} more objects in the scene."
        
        return description
    
    @staticmethod
    def _location_response(cv_data: Dict, query: str) -> str:
        """Generate location-based response."""
        objects = cv_data.get('objects', [])
        
        if not objects:
            return "I don't see any objects matching your query in the current view."
        
        # Try to find object mentioned in query
        query_words = query.lower().split()
        for obj in objects:
            if obj['class'].lower() in query_words or any(word in obj['class'].lower() for word in query_words):
                return (
                    f"I found a {obj['class']} at {obj['distance_m']:.1f} meters "
                    f"on your {obj['position']}."
                )
        
        # Return nearest object
        closest = objects[0]
        return (
            f"The nearest object is a {closest['class']} at {closest['distance_m']:.1f} meters "
            f"on your {closest['position']}."
        )
    
    @staticmethod
    def _brief_summary(cv_data: Dict) -> str:
        """Generate brief summary."""
        num_objects = cv_data.get('num_objects', 0)
        safety_status = cv_data.get('safety_status', 'UNKNOWN')
        
        if num_objects == 0:
            return "No objects detected in the current view."
        
        objects = cv_data.get('objects', [])
        closest = objects[0] if objects else None
        
        if closest:
            return (
                f"I detect {num_objects} object(s). "
                f"Closest is a {closest['class']} at {closest['distance_m']:.1f} meters. "
                f"Status: {safety_status}"
            )
        
        return f"I detect {num_objects} object(s). {safety_status}"
    
    @staticmethod
    def get_encouragement() -> str:
        """Get random encouragement message."""
        messages = [
            "I'm here to help you navigate safely.",
            "Feel free to ask me about your surroundings anytime.",
            "I'll keep you updated on any obstacles.",
            "Your safety is my priority.",
        ]
        return random.choice(messages)


