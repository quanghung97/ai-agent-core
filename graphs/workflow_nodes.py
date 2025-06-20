from typing import Dict, Any, List, Callable
from enum import Enum
import re
from utils.error_handling import with_retry, RetryableError, NodeExecutionError

class NodeType(Enum):
    CHAT = "chat"
    CLASSIFICATION = "classification"
    VALIDATION = "validation"
    SEARCH = "search"

class WorkflowNode:
    def __init__(self, processor: Callable, node_type: NodeType):
        self.processor = processor
        self.node_type = node_type
        
    @with_retry(max_retries=3, delay=1.0)
    async def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return await self.processor(state)
        except Exception as e:
            if isinstance(e, RetryableError):
                raise
            raise NodeExecutionError(f"Node execution failed: {str(e)}")

class WorkflowNodes:
    @staticmethod
    async def validate_input(state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize input"""
        try:
            message = state["messages"][-1]["content"]
            
            # Basic input validation
            if not message.strip():
                raise ValueError("Empty message")
                
            # Sanitize input
            message = re.sub(r'[^\w\s\?\!\.,]', '', message)
            state["messages"][-1]["content"] = message
            
            return state
        except Exception as e:
            raise NodeExecutionError(f"Validation failed: {str(e)}")

    @staticmethod
    @with_retry(max_retries=2, delay=0.5)
    async def classify_intent(state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            message = state["messages"][-1]["content"].lower()
            
            # Intent classification
            intents = {
                "greeting": ["hello", "hi", "hey", "xin chào"],
                "farewell": ["bye", "goodbye", "tạm biệt"],
                "question": ["what", "how", "why", "when", "where", "who"],
                "gratitude": ["thank", "thanks", "cảm ơn"]
            }
            
            detected_intent = "general"
            for intent, keywords in intents.items():
                if any(keyword in message for keyword in keywords):
                    detected_intent = intent
                    break
                    
            state["intent"] = detected_intent
            return state
        except Exception as e:
            raise RetryableError(f"Intent classification failed: {str(e)}")

