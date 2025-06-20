from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
import chromadb
from config.settings import get_settings
from datetime import datetime
import pytz

settings = get_settings()

class ConversationMemory:
    def __init__(self, user_id: str, agent_id: str, session_id: str):
        self.user_id = user_id
        self.agent_id = agent_id
        self.session_id = session_id
        self.collection_name = f"conversation_{user_id}_{session_id}_{agent_id}"
        self.client = None
        self.collection = None
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def initialize(self):
        """Initialize ChromaDB collection"""
        if not self.client:
            self.client = chromadb.HttpClient(
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT
            )
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API"""
        try:
            response = await self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")

    async def store_conversation(self, message: str, response: str, metadata: Dict[str, Any]):
        """Store conversation in ChromaDB"""
        if not self.collection:
            await self.initialize()

        # Add timestamp if not present
        if not metadata.get("timestamp"):
            metadata["timestamp"] = datetime.now(pytz.UTC).isoformat()

        # Combine message and response for context
        conversation_text = f"User: {message}\nAssistant: {response}"
        
        # Generate embedding
        embedding = await self.generate_embedding(conversation_text)

        # Store in ChromaDB
        self.collection.add(
            embeddings=[embedding],
            documents=[conversation_text],
            metadatas=[metadata],
            ids=[f"{self.session_id}_{metadata['timestamp']}"]
        )

    async def get_relevant_history(self, current_message: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant conversation history"""
        if not self.collection:
            await self.initialize()

        # Generate embedding for current message
        query_embedding = await self.generate_embedding(current_message)

        # Query ChromaDB for similar conversations
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"]
        )

        relevant_history = []
        for i in range(len(results["documents"][0])):      
            relevant_history.append({
                "conversation": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "relevance_score": 1 - results["distances"][0][i],
            })

        return relevant_history
