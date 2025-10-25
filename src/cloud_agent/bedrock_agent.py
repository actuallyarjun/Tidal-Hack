"""
AWS Bedrock Agent implementation for navigation assistance.
"""
from typing import Dict, List, Any
import numpy as np
from src.cloud_agent.agent_interface import AgentInterface
from src.cloud_agent.local_agent import LocalNavigationAgent
from config.settings import settings


class BedrockNavigationAgent(AgentInterface):
    """
    AWS Bedrock-powered navigation agent.
    Falls back to local agent if Bedrock is unavailable.
    """
    
    def __init__(self):
        """Initialize Bedrock agent and tools."""
        print("Initializing Bedrock Navigation Agent...")
        
        self.bedrock_available = False
        self.bedrock_client = None
        
        # Initialize fallback local agent
        self.local_agent = LocalNavigationAgent()
        
        # Try to initialize Bedrock if configured
        if settings.has_aws_credentials() and settings.use_bedrock and settings.has_bedrock_agent():
            try:
                import boto3
                
                self.bedrock_client = boto3.client(
                    'bedrock-agent-runtime',
                    aws_access_key_id=settings.aws_access_key_id,
                    aws_secret_access_key=settings.aws_secret_access_key,
                    region_name=settings.aws_region
                )
                
                self.bedrock_available = True
                print("✓ AWS Bedrock Agent initialized successfully")
                
            except Exception as e:
                print(f"Warning: Could not initialize Bedrock: {e}")
                print("Falling back to local agent.")
        else:
            print("Bedrock not configured. Using local agent.")
        
        # Conversation history
        self.conversation_history: List[Dict] = []
        self.session_id = "demo-session"
    
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
        # If Bedrock not available, use local agent
        if not self.bedrock_available:
            return self.local_agent.process_query(user_query, image_frame, cv_data)
        
        try:
            # Construct input with CV context
            cv_summary = self._format_cv_context(cv_data)
            bedrock_input = f"""User Query: {user_query}

Current Environment:
{cv_summary}

Provide a helpful, safety-focused response for navigation assistance."""
            
            # Invoke Bedrock Agent
            response_text = self.invoke_bedrock_agent(bedrock_input)
            
            # Generate haptic feedback based on CV data
            haptic_response = self._check_safety_alerts(cv_data)
            
            # Store in history
            self.conversation_history.append({
                'query': user_query,
                'response': response_text,
                'cv_data': cv_data,
                'used_bedrock': True
            })
            
            # Keep only last 5 exchanges
            if len(self.conversation_history) > 5:
                self.conversation_history = self.conversation_history[-5:]
            
            return {
                'text_response': response_text,
                'haptic_feedback': haptic_response,
                'safety_status': cv_data.get('safety_status', 'UNKNOWN'),
                'cv_summary': self._summarize_cv_data(cv_data),
                'used_bedrock': True
            }
            
        except Exception as e:
            print(f"Error invoking Bedrock agent: {e}")
            print("Falling back to local agent.")
            return self.local_agent.process_query(user_query, image_frame, cv_data)
    
    def invoke_bedrock_agent(self, user_input: str) -> str:
        """
        Invoke AWS Bedrock Agent.
        
        Args:
            user_input: User query with context
        
        Returns:
            Agent response text
        """
        if not self.bedrock_available or not self.bedrock_client:
            return "Bedrock Agent not available."
        
        try:
            response = self.bedrock_client.invoke_agent(
                agentId=settings.bedrock_agent_id,
                agentAliasId=settings.bedrock_agent_alias_id,
                sessionId=self.session_id,
                inputText=user_input
            )
            
            # Parse streaming response
            event_stream = response['completion']
            full_response = ""
            
            for event in event_stream:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        full_response += chunk['bytes'].decode('utf-8')
            
            return full_response if full_response else "No response from Bedrock agent."
            
        except Exception as e:
            print(f"Error invoking Bedrock agent: {e}")
            raise
    
    def _format_cv_context(self, cv_data: Dict) -> str:
        """Format CV data for Bedrock input."""
        num_objects = cv_data.get('num_objects', 0)
        safety_status = cv_data.get('safety_status', 'UNKNOWN')
        
        if num_objects == 0:
            return f"No objects detected. Safety Status: {safety_status}"
        
        lines = [f"Detected {num_objects} object(s). Safety Status: {safety_status}\n"]
        
        for obj in cv_data.get('objects', [])[:5]:  # Top 5
            dist_str = f"{obj['distance_m']:.1f}m" if obj['distance_m'] > 0 else "unknown"
            lines.append(f"  - {obj['class']} at {dist_str}, {obj['position']}")
        
        if cv_data.get('critical_alerts'):
            lines.append("\nCRITICAL ALERTS:")
            for alert in cv_data['critical_alerts']:
                lines.append(f"  ⚠ {alert['class']} only {alert['distance_m']:.1f}m away!")
        
        return "\n".join(lines)
    
    def _check_safety_alerts(self, cv_data: Dict) -> Dict:
        """Check for immediate safety hazards."""
        from src.cloud_agent.tools import NavigationTools
        
        critical_alerts = cv_data.get('critical_alerts', [])
        
        if len(critical_alerts) > 0:
            closest = critical_alerts[0]
            return NavigationTools.haptic_feedback_tool(
                closest['distance_m'],
                closest['position']
            )
        
        return {'enabled': False}
    
    def _summarize_cv_data(self, cv_data: Dict) -> Dict:
        """Create summary of CV data."""
        return {
            'total_objects': cv_data.get('num_objects', 0),
            'critical_count': len(cv_data.get('critical_alerts', [])),
            'safety_status': cv_data.get('safety_status', 'UNKNOWN')
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        if self.bedrock_available:
            return self.conversation_history
        else:
            return self.local_agent.get_conversation_history()
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.local_agent.clear_history()
        print("Conversation history cleared")

