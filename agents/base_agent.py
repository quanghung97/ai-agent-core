from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.created_at = datetime.utcnow()
        self.session_data: Dict[str, Any] = {}
        
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize agent resources"""
        pass
    
    # @abstractmethod
    # async def process_message(
    #     self,
    #     user_id: str,
    #     message: str,
    #     session_id: str,
    #     context: Optional[Dict[str, Any]] = None
    # ) -> Dict[str, Any]:
    #     """Process incoming message"""
    #     pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        pass
