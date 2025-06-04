import asyncio
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits

async def main():
    # Create personality
    personality = PersonalityConfig(
        name="Luna",
        gender="female",
        age=25,
        personality_traits=PersonalityTraits(
            friendliness=0.9,
            humor=0.7,
            formality=0.3,
            creativity=0.8
        ),
        interests=["technology", "music", "travel"],
        communication_style="casual_friendly"
    )
    
    # Create and initialize chat agent
    agent = ChatAgent("agent-001", personality)
    await agent.initialize()
    
    # Test conversation
    response = await agent.process_message(
        user_id="user-001",
        message="Xin chào! Bạn có thể giới thiệu về bản thân được không?",
        session_id="session-001"
    )
    
    print("AI Response:", response["response"])

if __name__ == "__main__":
    asyncio.run(main())
