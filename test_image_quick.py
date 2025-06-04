import asyncio
import logging
from agents.image_agent import ImageAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits

logging.basicConfig(level=logging.INFO)

async def main():
    # Create personality
    personality = PersonalityConfig(
        name="Artista",
        gender="female",
        age=25,
        personality_traits=PersonalityTraits(
            creativity=0.9,
            detail_oriented=0.8,
            friendliness=0.7,
            humor=0.5,
            formality=0.3
        ),
        interests=["digital art", "photography"],
        communication_style="creative",
        artistic_style="digital art, vibrant colors",
        language="vi"
    )
    
    # Create agent
    gen_agent = ImageAgent("gen-test-agent", personality)
    
    try:
        # Generate a test image
        print("Generating image...")
        result = await gen_agent.process_message(
            user_id="test-user",
            session_id="test-session",
            message='''{"operation": "generate", 
                       "prompt": "An empty coffee shop in Hanoi",
                       "size": "1024x1024",
                       "model": "gpt-image-1",
                       "quality": "high"}'''
        )
        
        if result["type"] == "image":
            print(f"\nImage generated successfully!")
            print(f"Image URL: {result['metadata']['image_url']}")
            print(f"Model used: {result['metadata']['model']}")
            print(f"Style applied: {result['metadata']['style']}")
        else:
            print(f"\nError: {result['response']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await gen_agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
