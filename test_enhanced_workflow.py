import asyncio
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits
from memory.knowledge_memory import KnowledgeMemory
import uuid
import os
import json

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

async def test_conversation_flow():
    """Test the conversation flow with enhanced workflow and search capability"""
    # Create personality configuration
    personality = PersonalityConfig(
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
        interests=["technology", "world news", "environment"],
        communication_style="casual_friendly",
        language="en",
        artistic_style="modern",
    )
    
    # Create and initialize agent
    agent = ChatAgent("agent-001", personality)
    await agent.initialize()
    
    try:
        # Load knowledge base directly with JSON data
        await agent.knowledge_memory.load_knowledge_base(sample_knowledge)
        print("Knowledge base loaded successfully")
        
        session_id = str(uuid.uuid4())
        user_id = "user-001"
        
        # Test scenarios
        scenarios = [
            "What's happening with global trade in 2025?",
            # "Tell me about recent AI developments.",
        ]

        # Run test scenarios
        for message in scenarios:
            print(f"\nUser: {message}")
            response = await agent.process_message(
                user_id=user_id,
                message=message,
                session_id=session_id,
                tts_settings={"enable_tts": False}
            )
            print(f"AI: {response['response']}")
            print(f"Intent: {response.get('metadata', {}).get('intent', 'unknown')}")
            print(f"Turn count: {response.get('metadata', {}).get('memory', {}).get('turn_count', 0)}")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    import os
    os.makedirs("data/chromadb", exist_ok=True)
    asyncio.run(test_conversation_flow())
