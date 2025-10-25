"""
Abstract interface for navigation agents.
Allows swapping between local and cloud implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np


class AgentInterface(ABC):
    """Abstract base class for navigation agents."""
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        pass
    
    @abstractmethod
    def clear_history(self):
        """Clear conversation history."""
        pass
    
    def get_agent_type(self) -> str:
        """Get agent type identifier."""
        return self.__class__.__name__


