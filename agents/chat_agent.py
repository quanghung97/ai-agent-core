from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent
from models.openai_models import OpenAIChat
from models.tts_models import TextToSpeechModel
from personality.personality_config import PersonalityConfig
from core.session_manager import SessionManager
from graphs.chat_graph import ChatWorkflow
from utils.error_handling import NodeExecutionError, WorkflowError
import logging

logger = logging.getLogger(__name__)

class ChatAgent(BaseAgent):
    def __init__(self, agent_id: str, personality: PersonalityConfig):
        super().__init__(agent_id)
        self.personality = personality
        self.openai_chat = OpenAIChat()
        self.tts_model = TextToSpeechModel()
        self.session_manager = SessionManager()
        self.workflow = ChatWorkflow(self.openai_chat, self.personality)
        self.graph = self.workflow.create_graph()
    
    async def initialize(self) -> None:
        """Initialize agent resources"""
        await self.session_manager.initialize()
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None,
        tts_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            # Get or create session
            session = await self.session_manager.get_session(session_id)
            if not session:
                session = await self.session_manager.create_session(session_id, user_id)
            
            # Ensure session has messages array
            if "messages" not in session:
                session["messages"] = []
            
            # Add user message
            session["messages"].append({
                "role": "user",
                "content": message
            })
            
            # Process through workflow graph
            result = await self.workflow.run({
                "messages": session["messages"],
                "user_id": user_id,
                "session_id": session_id,
                "context": context or {}
            })

            if not result or "response" not in result:
                raise WorkflowError("Invalid workflow response")

            # Update session with new messages
            session["messages"] = result.get("messages", session["messages"])
            await self.session_manager.update_session(session_id, session)

            response_text = result["response"].get("response", "An error occurred")
            
            # Generate speech if TTS settings are provided
            audio_data = None
            if tts_settings and tts_settings.get('enable_tts'):
                try:
                    audio_data = await self.tts_model.generate_speech(
                        text=response_text,
                        voice_id=tts_settings.get('voice_id'),
                        voice_settings=tts_settings.get('voice_settings')
                    )
                except Exception as e:
                    logger.error(f"Text-to-speech generation failed: {str(e)}")
                    # Continue without audio if TTS fails
        
            return {
                "response": response_text,
                "session_id": session_id,
                "user_id": user_id,
                "type": result["response"].get("type", "error"),
                "metadata": result["response"].get("metadata", {}),
                "audio": audio_data if audio_data else None
            }
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "response": "An unexpected error occurred. Please try again later.",
                "session_id": session_id,
                "user_id": user_id,
                "type": "error",
                "metadata": {"error": "Internal server error"},
                "audio": None
            }
    
    async def cleanup(self) -> None:
        pass
