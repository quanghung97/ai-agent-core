from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent
from models.openai_models import OpenAIChat
from models.tts_models import TextToSpeechModel
from personality.personality_config import PersonalityConfig
from graphs.chat_graph import ChatWorkflow
from utils.error_handling import NodeExecutionError, WorkflowError
from memory.knowledge_memory import KnowledgeMemory
from memory.conversation_memory import ConversationMemory
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)

class ChatAgent(BaseAgent):
    def __init__(self, agent_id: str, personality: PersonalityConfig):
        super().__init__(agent_id)
        self.personality = personality
        self.openai_chat = OpenAIChat()
        self.tts_model = TextToSpeechModel()
        self.knowledge_memory = KnowledgeMemory(f"knowledge_base_{agent_id}")
        self.conversation_memories: Dict[str, ConversationMemory] = {}
        self.workflow = ChatWorkflow(self.openai_chat, self.personality, self.knowledge_memory)
        self.graph = self.workflow.create_graph()

    async def initialize(self) -> None:
        """Initialize agent resources"""
        await self.knowledge_memory.initialize()
    
    async def get_conversation_memory(self, user_id: str, session_id: str) -> ConversationMemory:
        memory_key = f"{user_id}_{session_id}"
        if memory_key not in self.conversation_memories:
            memory = ConversationMemory(user_id, self.agent_id, session_id)
            await memory.initialize()
            self.conversation_memories[memory_key] = memory
        return self.conversation_memories[memory_key]

    async def process_message(
        self,
        user_id: str,
        message: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None,
        tts_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            # Get conversation memory
            conversation_memory = await self.get_conversation_memory(user_id, session_id)

            # Get relevant conversation history
            relevant_history = await conversation_memory.get_relevant_history(message)
            
            # Add relevant history to context
            if relevant_history:
                context = context or {}
                context["relevant_history"] = relevant_history

            # Process through workflow graph
            result = await self.workflow.run({
                "messages": [{
                    "role": "user",
                    "content": message
                }],
                "user_id": user_id,
                "session_id": session_id,
                "context": context or {}
            })

            if not result or "response" not in result:
                raise WorkflowError("Invalid workflow response")

            response_obj = result.get("response")
            if isinstance(response_obj, dict):
                response_text = response_obj.get("response", "An error occurred")
                response_type = response_obj.get("type", "error")
            else:
                logger.error(f"Unexpected response format: {response_obj}")
                response_text = str(response_obj) if response_obj else "An error occurred"
                response_type = "error"
            print(f"Response text: {tts_settings}")
            # Generate speech if TTS settings are provided
            audio_data = None
            if tts_settings and getattr(tts_settings, 'enable_tts', False):
                try:
                    audio_data = await self.tts_model.generate_speech(
                        text=response_text,
                        voice_id=tts_settings.get('voice_id'),
                        voice_settings=tts_settings.get('voice_settings')
                    )
                except Exception as e:
                    logger.error(f"Text-to-speech generation failed: {str(e)}")

            return {
                "response": response_text,
                "session_id": session_id,
                "user_id": user_id,
                "type": response_type,
                "metadata": {
                    "timestamp": datetime.now(pytz.UTC).isoformat()
                },
                "audio": audio_data if audio_data else None
            }
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            current_time = datetime.now(pytz.UTC).isoformat()
            return {
                "response": "An unexpected error occurred. Please try again later.",
                "session_id": session_id,
                "user_id": user_id,
                "type": "error",
                "metadata": {
                    "error": "Internal server error",
                    "timestamp": current_time
                },
                "audio": None
            }
    
    async def cleanup(self) -> None:
        pass
