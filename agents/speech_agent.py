from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from .chat_agent import ChatAgent
from models.speech_models import SpeechToTextModel
from graphs.speech_graph import SpeechWorkflow
from personality.personality_config import PersonalityConfig
import logging

logger = logging.getLogger(__name__)

class SpeechAgent(BaseAgent):
    """Agent that handles speech-to-text and chat processing"""
    
    def __init__(self, agent_id: str, personality: PersonalityConfig):
        super().__init__(agent_id)
        self.personality = personality
        self.speech_model = SpeechToTextModel()
        self.speech_workflow = SpeechWorkflow(self.speech_model)
        self.chat_agent = ChatAgent(f"{agent_id}-chat", personality)
        
    async def initialize(self) -> None:
        """Initialize agent resources"""
        await self.chat_agent.initialize()
        
    async def process_message(
        self,
        user_id: str,
        audio_url: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process audio message through speech-to-text and chat"""
        try:
            # First convert speech to text
            speech_result = await self.speech_workflow.run({
                "audio_url": audio_url
            })
            
            if not speech_result.get("text"):
                raise Exception("Speech transcription failed")
                
            # Then process the text through chat agent
            chat_result = await self.chat_agent.process_message(
                user_id=user_id,
                message=speech_result["text"],
                session_id=session_id,
                context=context
            )
            
            # Combine results
            return {
                **chat_result,
                "transcription": {
                    "text": speech_result["text"],
                    "language": speech_result["language"],
                    "confidence": speech_result["confidence"]
                }
            }
            
        except Exception as e:
            logger.error(f"Speech processing failed: {str(e)}")
            return {
                "response": "Failed to process audio message",
                "session_id": session_id,
                "user_id": user_id,
                "type": "error",
                "metadata": {"error": str(e)}
            }
            
    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        await self.chat_agent.cleanup()
