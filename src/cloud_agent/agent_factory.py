"""
Factory for creating the appropriate navigation agent.
"""
from src.cloud_agent.agent_interface import AgentInterface
from src.cloud_agent.local_agent import LocalNavigationAgent
from src.cloud_agent.bedrock_agent import BedrockNavigationAgent
from config.settings import settings


class AgentFactory:
    """Factory for creating navigation agents."""
    
    @staticmethod
    def create_agent() -> AgentInterface:
        """
        Create the appropriate navigation agent based on configuration.
        
        Returns:
            AgentInterface: Configured navigation agent
        """
        # Check if Bedrock is configured and enabled
        if settings.use_bedrock and settings.has_bedrock_agent() and settings.has_aws_credentials():
            print("Creating Bedrock Navigation Agent...")
            return BedrockNavigationAgent()
        
        # Default to local agent
        print("Creating Local Navigation Agent...")
        return LocalNavigationAgent()
    
    @staticmethod
    def create_local_agent() -> LocalNavigationAgent:
        """Create a local navigation agent explicitly."""
        return LocalNavigationAgent()
    
    @staticmethod
    def create_bedrock_agent() -> BedrockNavigationAgent:
        """Create a Bedrock navigation agent explicitly."""
        return BedrockNavigationAgent()
    
    @staticmethod
    def get_available_agents() -> list:
        """
        Get list of available agent types.
        
        Returns:
            list: Available agent type names
        """
        available = ['LocalNavigationAgent']
        
        if settings.has_aws_credentials() and settings.has_bedrock_agent():
            available.append('BedrockNavigationAgent')
        
        return available

