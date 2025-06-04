import asyncio
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits
import uuid
import os

async def test_conversation_flow():
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
        interests=["technology", "music", "travel"],
        communication_style="casual_friendly",
        artistic_style="modern",
    )
    
    # Create and initialize agent
    agent = ChatAgent("agent-001", personality)
    try:
        await agent.initialize()
    except Exception as e:
        print(f"Failed to initialize agent: {str(e)}")
        return
        
    session_id = str(uuid.uuid4())
    user_id = "user-001"
    
    # Test different conversation scenarios
    # scenarios = [
    #     # Greeting
    #     "Xin chào Luna! Rất vui được gặp bạn.",
    #     # Question
    #     "Bạn có thể giúp tôi học lập trình Python không?",
    #     # Technical discussion
    #     "Sự khác biệt giữa list và tuple trong Python là gì?",
    #     # Gratitude
    #     "Cảm ơn bạn rất nhiều về những thông tin hữu ích!",
    #     # Farewell
    #     "Tạm biệt nhé!"
    # ]
    
    scenarios = [
        "Chào Luna, hôm nay của bạn thế nào?"
        # "Diễn biến tình hình sự kiện Trump đánh thuế lên hàng hóa Trung Quốc 2025",
        # Question
        # "Phản ứng của Trung Quốc là gì?",
        # # Technical discussion
        # "Ảnh hương của sự kiện này đến nền kinh tế toàn cầu là gì?",
        # # Gratitude
        # "Các chyên gia cho rằng đây là một bước đi đúng đắn hay sai lầm?",
        # # Farewell
        # "Cảm ơn!"
    ]

    # Enable TTS for testing
    voice_settings = {
        "stability": 0.7,
        "similarity_boost": 0.7,
        "style": 0.0,
        "use_speaker_boost": True,
        "speed": 1.0
    }

    for message in scenarios:
        print(f"\nUser: {message}")
        response = await agent.process_message(
            user_id=user_id,
            message=message,
            session_id=session_id,
            enable_tts=True,  # Enable TTS
            voice_id="1l0C0QA9c9jN22EmWiB0",  # Optional: specific voice
            voice_settings=voice_settings  # Optional: voice settings
        )
        print(f"AI: {response['response']}")
        print(f"Intent: {response.get('metadata', {}).get('intent', 'unknown')}")
        print(f"Turn count: {response.get('metadata', {}).get('memory', {}).get('turn_count', 0)}")
        
        # Save audio if present
        if response.get('audio'):
            os.makedirs('output', exist_ok=True)
            with open(f'output/response_{response.get("metadata", {}).get("memory", {}).get("turn_count", 0)}.mp3', 'wb') as f:
                f.write(response['audio'])
            print(f"Audio saved for turn {response.get('metadata', {}).get('memory', {}).get('turn_count', 0)}")

if __name__ == "__main__":
    asyncio.run(test_conversation_flow())
