import asyncio
import logging
from agents.speech_agent import SpeechAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits
import uuid

logging.basicConfig(level=logging.INFO)

async def test_speech_workflow():
    # Create personality
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
        language="vi"
    )
    
    # Create agent
    agent = SpeechAgent("speech-test-agent", personality)
    await agent.initialize()
    
    try:
        # Test with audio file
        session_id = str(uuid.uuid4())
        result = await agent.process_message(
            user_id="test-user",
            audio_url="https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3",  # Replace with actual audio URL
            session_id=session_id
        )
        
        print("\nTranscription:", result["transcription"]["text"])
        print("Language:", result["transcription"]["language"])
        print("AI Response:", result["response"])
        print("Intent:", result.get("metadata", {}).get("intent", "unknown"))
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(test_speech_workflow())
