import grpc
import asyncio
from typing import Dict
from services.chats.chat_service_pb2 import ChatRequest, ChatResponse, Metadata
from services.chats.chat_service_pb2_grpc import ChatServiceServicer
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig
from memory.redis_store import RedisStore
import logging
import json

logger = logging.getLogger(__name__)

# # Sample knowledge data for different domains
# sample_knowledge = [
#     {
#         "id": "news_001",
#         "text": "In 2025, global trade tensions escalated as new tariff policies were implemented between major economies.",
#         "metadata": {
#             "topic": "Economics",
#             "source": "Global News",
#             "tags": "trade,economy,international relations",
#             "date": "2025-06-01"
#         }
#     },
#     {
#         "id": "news_002",
#         "text": "The technology sector saw significant growth in AI adoption across industries, with particular focus on responsible AI development.",
#         "metadata": {
#             "topic": "Technology",
#             "source": "Tech Review",
#             "tags": "AI,technology,industry",
#             "date": "2025-06-01"
#         }
#     },
#     {
#         "id": "news_003",
#         "text": "Climate change initiatives gained momentum as countries accelerated their transition to renewable energy sources.",
#         "metadata": {
#             "topic": "Environment",
#             "source": "Climate Report",
#             "tags": "climate,energy,sustainability",
#             "date": "2025-06-01"
#         }
#     },
# ]

class ChatServiceImpl(ChatServiceServicer):
    """Implementation of gRPC Chat Service"""
    
    def __init__(self):
        # Redis setup
        self.redis_store = RedisStore()
        
        # Cache for active chat agents
        self._chat_agents: Dict[str, ChatAgent] = {}
        self._initialized = False
        self._init_lock = asyncio.Lock()

    async def get_or_create_chat_agent(self, agent_id: str) -> ChatAgent:
        """Get existing chat agent or create new one"""
        if agent_id not in self._chat_agents:
            # Get agent config from Redis
            config_data = await self.redis_store.get(f"agent:{agent_id}:config")
            if not config_data:
                raise ValueError(f"Agent with id {agent_id} not found in Redis")
            
            # Convert Redis data to PersonalityConfig
            config = PersonalityConfig(**config_data.get('value', {}))

            # Create new chat agent
            chat_agent = ChatAgent(agent_id, config)
            await chat_agent.initialize()
            # TODO: load knowledge base func
            # await chat_agent.knowledge_memory.load_knowledge_base(sample_knowledge)
            self._chat_agents[agent_id] = chat_agent

        return self._chat_agents[agent_id]

    async def ProcessMessage(self, request: ChatRequest, context):
        """Process a single chat message with specified agent"""
        try:
            # Get or create chat agent for the specified agent_id
            chat_agent = await self.get_or_create_chat_agent(request.agent_id)

            # Parse recent_history JSON string if present
            context_dict = {}
            if request.recent_history:
                try:
                    context_dict["recent_conversations"] = json.loads(request.recent_history)
                except Exception as e:
                    logger.warning(f"Failed to parse recent_history: {e}")

            result = await chat_agent.process_message(
                user_id=request.user_id,
                message=request.message,
                session_id=request.session_id,
                context=context_dict,
                tts_settings=request.tts_settings if request.HasField('tts_settings') else None
            )

            # Only use timestamp for metadata
            metadata = Metadata(timestamp=result["metadata"].get("timestamp", ""))

            return ChatResponse(
                response=result.get("response", ""),
                session_id=result.get("session_id", ""),
                user_id=result.get("user_id", ""),
                type=result.get("type", "text"),
                metadata=metadata,
                audio_content=result.get('audio', b''),
                error=""  # Optionally set error
            )
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return ChatResponse(
                response="",
                session_id="",
                user_id="",
                type="error",
                metadata=Metadata(timestamp=""),
                audio_content=b"",
                error=str(e)
            )
