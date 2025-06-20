from services.vector_store.vector_store_service_pb2_grpc import VectorStoreServiceServicer
from services.vector_store.vector_store_service_pb2 import StoreConversationRequest, StoreConversationResponse
from memory.conversation_memory import ConversationMemory
import logging

logger = logging.getLogger(__name__)

class VectorStoreServiceImpl(VectorStoreServiceServicer):
    def __init__(self):
        self.memories = {}

    async def StoreConversation(self, request: StoreConversationRequest, context):
        try:
            memory_key = f"{request.user_id}_{request.session_id}_{request.agent_id}"
            if memory_key not in self.memories:
                memory = ConversationMemory(
                    user_id=request.user_id,
                    agent_id=request.agent_id,
                    session_id=request.session_id
                )
                await memory.initialize()
                self.memories[memory_key] = memory

            # Only use timestamp from metadata
            metadata = {
                "timestamp": request.metadata.timestamp
            }

            await self.memories[memory_key].store_conversation(
                message=request.message,
                response=request.response,
                metadata=metadata
            )

            return StoreConversationResponse(success=True)
        except Exception as e:
            logger.error(f"Failed to store conversation: {str(e)}")
            return StoreConversationResponse(
                success=False,
                error=str(e)
            )
