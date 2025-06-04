from typing import Dict, Any, Optional
from langgraph.graph import Graph

class BaseWorkflow:
    """Base class for all workflow graphs"""
    
    def __init__(self):
        self.graph = Graph()
        
    def create_graph(self) -> Graph:
        """Create and return the workflow graph"""
        raise NotImplementedError
    
    @staticmethod
    def format_response(response: str) -> Dict[str, Any]:
        """Format the response for consistent output"""
        return {
            "response": response,
            "type": "text",
            "metadata": {}
        }
