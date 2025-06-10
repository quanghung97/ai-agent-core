import grpc
import asyncio
from concurrent import futures
from typing import Dict, Any
from services.chats.chat_service_pb2 import ChatRequest, ChatResponse, MetadataMessage, TTSSettings, VoiceSettings
from services.chats.chat_service_pb2_grpc import ChatServiceServicer
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits
import logging
import json

logger = logging.getLogger(__name__)

# Sample knowledge data for different domains
sample_knowledge = [
    {
        "id": "news_001",
        "text": "In 2025, global trade tensions escalated as new tariff policies were implemented between major economies.",
        "metadata": {
            "topic": "Economics",
            "source": "Global News",
            "tags": "trade,economy,international relations",
            "date": "2025-06-01"
        }
    },
    {
        "id": "news_002",
        "text": "The technology sector saw significant growth in AI adoption across industries, with particular focus on responsible AI development.",
        "metadata": {
            "topic": "Technology",
            "source": "Tech Review",
            "tags": "AI,technology,industry",
            "date": "2025-06-01"
        }
    },
    {
        "id": "news_003",
        "text": "Climate change initiatives gained momentum as countries accelerated their transition to renewable energy sources.",
        "metadata": {
            "topic": "Environment",
            "source": "Climate Report",
            "tags": "climate,energy,sustainability",
            "date": "2025-06-01"
        }
    },
]

class ChatServiceImpl(ChatServiceServicer):
    """Implementation of gRPC Chat Service"""
    
    def __init__(self):
        self.personality = PersonalityConfig(
            name="Luna",
            gender="female",
            age=25,
            personality_traits=PersonalityTraits(
                friendliness=0.9,
                humor=0.7,
                formality=0.3,
                creativity=0.8,
                detail_oriented=0.6,
            ),
            interests=["technology", "music", "travel"],
            communication_style="casual_friendly",
            artistic_style="modern",
        )
        self.chat_agent = ChatAgent("grpc-agent", self.personality)
        self._initialized = False
        self._init_lock = asyncio.Lock()
        
        # Start initialization
        asyncio.create_task(self.ensure_initialized())

    async def ensure_initialized(self):
        """Ensure the service is initialized only once"""
        async with self._init_lock:
            if not self._initialized:
                try:
                    # Initialize chat agent
                    await self.chat_agent.initialize()
                    
                    # Load knowledge base
                    await self.chat_agent.knowledge_memory.load_knowledge_base(sample_knowledge)
                    logger.info("Knowledge base loaded successfully")
                    
                    self._initialized = True
                    logger.info("Chat service initialization completed")
                except Exception as e:
                    logger.error(f"Failed to initialize chat service: {str(e)}")
                    raise

    async def cleanup(self):
        """Cleanup resources"""
        if self.chat_agent and self.chat_agent.knowledge_memory:
            await self.chat_agent.knowledge_memory.cleanup()
            logger.info("Chat service resources cleaned up")

    async def ProcessMessage(self, request: ChatRequest, context):
        """Process a single chat message - async implementation"""
        try:
            # Ensure service is initialized
            if not self._initialized:
                await self.ensure_initialized()

            tts_settings = None
            if request.tts_settings and request.tts_settings.enable_tts:
                tts_settings = {
                    'enable_tts': request.tts_settings.enable_tts,
                    'voice_id': request.tts_settings.voice_id,
                    'voice_settings': {
                        'stability': request.tts_settings.voice_settings.stability,
                        'similarity_boost': request.tts_settings.voice_settings.similarity_boost,
                        'style': request.tts_settings.voice_settings.style,
                        'use_speaker_boost': request.tts_settings.voice_settings.use_speaker_boost,
                        'speed': request.tts_settings.voice_settings.speed
                    }
                }

            result = await self.chat_agent.process_message(
                user_id=request.user_id,
                message=request.message,
                session_id=request.session_id,
                context=dict(request.context),
                tts_settings=tts_settings
            )
            
            metadata = MetadataMessage(
                intent=result.get("metadata", {}).get("intent", ""),
                turn_count=result.get("metadata", {}).get("memory", {}).get("turn_count", 0),
                additional_data={
                    k: str(v) for k, v in result.get("metadata", {}).items() 
                    if k not in ["intent", "memory"]
                }
            )
            
            return ChatResponse(
                response=result.get("response", ""),
                session_id=result.get("session_id", ""),
                user_id=result.get("user_id", ""),
                type=result.get("type", "text"),
                metadata=metadata,
                audio_content=result.get('audio', b'')
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            raise

    async def StreamChat(self, request_iterator, context):
        """Handle streaming chat - async implementation"""
        try:
            async for request in request_iterator:
                response = await self.ProcessMessage(request, context)
                yield response
                
        except Exception as e:
            logger.error(f"Error in stream chat: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Stream error: {str(e)}")
            raise
