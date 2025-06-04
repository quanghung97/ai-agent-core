import asyncio
import pytest
from agents.image_agent import ImageAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits

async def test_image_generation():
    # Create artistic personality
    personality = PersonalityConfig(
        name="Artista",
        gender="female",
        age=25,
        personality_traits=PersonalityTraits(
            friendliness=0.8,
            humor=0.6,
            formality=0.4,
            creativity=0.9,
            detail_oriented=0.8,
        ),
        interests=["digital art", "photography", "modern design"],
        communication_style="creative",
        artistic_style="digital art, vibrant colors, highly detailed",
        language="vi"
    )
    
    # Initialize agent
    agent = ImageAgent("test-image-agent", personality)
    
    # Test scenarios
    scenarios = [
        {
            "prompt": "Một khu vườn Việt Nam truyền thống với hoa sen và đèn lồng",
            "size": "1024x1024",
            "model": "dall-e-3",
            "style": "watercolor painting"
        },
        {
            "prompt": "Phố cổ Hà Nội vào buổi sáng sớm với những người bán hàng rong",
            "size": "1792x1024",  # Landscape format
            "model": "dall-e-3",
            "style": "photorealistic"
        },
        {
            "prompt": "Một quán cà phê hiện đại ở Sài Gòn với kiến trúc độc đáo",
            "size": "1024x1024",
            "model": "dall-e-3",
            "style": "modern architectural visualization"
        }
    ]
    
    try:
        for scenario in scenarios:
            print(f"\nGenerating image for prompt: {scenario['prompt']}")
            result = await agent.generate_image(
                prompt=scenario["prompt"],
                size=scenario["size"],
                model=scenario["model"],
                style=scenario["style"]
            )
            
            print(f"Generated image URL: {result['image_url']}")
            print("Personality influence:", result["result"]["personality_influence"])
            print("Style applied:", result["result"]["style"])
            
            # Optional: Test image editing
            if result.get("image_url"):
                edit_result = await agent.edit_image(
                    image_url=result["image_url"],
                    prompt="Thêm vài người đang thưởng thức cà phê vào khung cảnh"
                )
                print(f"Edited image URL: {edit_result['image_url']}")
                
    except Exception as e:
        print(f"Error during image generation: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_image_generation())