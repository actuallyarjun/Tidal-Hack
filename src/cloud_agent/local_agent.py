"""
Local agent implementation for navigation assistance.
"""
from typing import Dict, List, Any
import numpy as np
from src.cloud_agent.agent_interface import AgentInterface
from src.cloud_agent.gemini_tool import GeminiVLMTool
from src.cloud_agent.tools import NavigationTools
from src.cloud_agent.mock_responses import MockResponseGenerator


class LocalNavigationAgent(AgentInterface):
    """
    Local navigation agent with optional VLM enhancement.
    Orchestrates CV data, VLM, and navigation tools.
    """
    
    def __init__(self):
        """Initialize local agent and tools."""
        print("Initializing Local Navigation Agent...")
        
        # Initialize tools
        self.gemini_tool = GeminiVLMTool()
        self.nav_tools = NavigationTools()
        
        # Conversation history for context
        self.conversation_history: List[Dict] = []
        
        print(f"✓ Local Agent initialized (Gemini available: {self.gemini_tool.is_available()})")
    
    def process_query(
        self, 
        user_query: str, 
        image_frame: np.ndarray,
        cv_data: Dict
    ) -> Dict[str, Any]:
        """
        Process user query with multimodal context.
        
        Args:
            user_query: User's spoken/typed query
            image_frame: Current camera frame
            cv_data: Structured CV detection data
        
        Returns:
            Agent response with text and actions
        """
        try:
            # Step 1: Process CV data
            processed_cv = self.nav_tools.cv_perception_tool(cv_data)
            
            # Step 2: Check for immediate safety alerts
            haptic_response = self._check_safety_alerts(processed_cv)
            
            # Step 3: Determine if VLM is needed
            needs_vlm = self._should_use_vlm(user_query)
            
            if needs_vlm and self.gemini_tool.is_available():
                # Use Gemini for semantic understanding
                description = self.gemini_tool.generate_description(
                    image_frame,
                    processed_cv,
                    user_query
                )
            else:
                # Use simple rule-based response for quick queries
                description = MockResponseGenerator.generate_description(
                    processed_cv, 
                    user_query
                )
            
            # Step 4: Add to conversation history
            self.conversation_history.append({
                'query': user_query,
                'response': description,
                'cv_data': processed_cv,
                'used_vlm': needs_vlm and self.gemini_tool.is_available()
            })
            
            # Keep only last 5 exchanges
            if len(self.conversation_history) > 5:
                self.conversation_history = self.conversation_history[-5:]
            
            return {
                'text_response': description,
                'haptic_feedback': haptic_response,
                'safety_status': processed_cv['safety_status'],
                'cv_summary': self._summarize_cv_data(processed_cv),
                'used_vlm': needs_vlm and self.gemini_tool.is_available()
            }
            
        except Exception as e:
            print(f"Error in agent processing: {e}")
            return {
                'text_response': f"I encountered an error processing your request. Please try again.",
                'haptic_feedback': {'enabled': False},
                'safety_status': 'UNKNOWN',
                'cv_summary': {},
                'error': str(e)
            }
    
    def _check_safety_alerts(self, cv_data: Dict) -> Dict:
        """Check for immediate safety hazards and generate haptic feedback."""
        critical_alerts = cv_data.get('critical_alerts', [])
        
        if len(critical_alerts) > 0:
            # Get closest obstacle
            closest = critical_alerts[0]
            return self.nav_tools.haptic_feedback_tool(
                closest['distance_m'],
                closest['position']
            )
        
        return {'enabled': False}
    
    def _should_use_vlm(self, query: str) -> bool:
        """Determine if query requires VLM processing."""
        # Keywords that suggest need for detailed semantic understanding
        vlm_keywords = [
            'describe', 'what', 'where', 'how many', 'tell me about',
            'explain', 'identify', 'recognize', 'scene', 'environment',
            'see', 'look', 'show', 'detail', 'color', 'appearance'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in vlm_keywords)
    
    def _summarize_cv_data(self, cv_data: Dict) -> Dict:
        """Create summary of CV data for UI display."""
        return {
            'total_objects': cv_data.get('num_objects', 0),
            'critical_count': len(cv_data.get('critical_alerts', [])),
            'safety_status': cv_data.get('safety_status', 'UNKNOWN'),
            'objects_by_position': self._group_objects_by_position(cv_data)
        }
    
    def _group_objects_by_position(self, cv_data: Dict) -> Dict:
        """Group objects by position for easy UI display."""
        objects = cv_data.get('objects', [])
        grouped = {'left': [], 'center': [], 'right': []}
        
        for obj in objects:
            pos = obj.get('position', 'center')
            if pos in grouped:
                grouped[pos].append(obj['class'])
        
        return grouped
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("Conversation history cleared")

