import asyncio
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits
import uuid

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
    
    # Create chat agent
    agent = ChatAgent("agent-001", personality)
    session_id = str(uuid.uuid4())
    user_id = "user-001"
    
    # Test multiple messages in same session
    messages = [
        "Xin chào! Bạn có thể giới thiệu về bản thân được không?",
        "Bạn thích làm gì trong thời gian rảnh?",
        "Cảm ơn cuộc trò chuyện nhé!"
    ]
    
    for message in messages:
        response = await agent.process_message(
            user_id=user_id,
            message=message,
            session_id=session_id
        )
        print(f"\nUser: {message}")
        print(f"AI: {response['response']}")

if __name__ == "__main__":
    asyncio.run(main())
