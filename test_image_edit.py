import asyncio
import logging
from agents.image_agent import ImageAgent
from agents.edit_image_agent import EditImageAgent
from personality.personality_config import PersonalityConfig, PersonalityTraits

logging.basicConfig(level=logging.INFO)

async def test_image_edit():
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
    
    # Create agents
    gen_agent = ImageAgent("gen-test-agent", personality)
    edit_agent = EditImageAgent("edit-test-agent", personality)
    
    try:
        # First generate an image to edit
        print("=" * 60)
        print("STEP 1: Generating initial image...")
        print("=" * 60)
        
        gen_result = await gen_agent.process_message(
            user_id="test-user",
            session_id="test-session",
            message='''{"operation": "generate", 
                       "prompt": "An empty coffee shop in Hanoi",
                       "size": "1024x1024",
                       "model": "dall-e-3",
                       "quality": "hd"}'''
        )
        
        if gen_result["type"] != "image":
            raise Exception("Failed to generate initial image")
            
        initial_image_url = gen_result["metadata"]["image_url"]
        print(f"✅ Initial image generated successfully!")
        print(f"   URL: {initial_image_url}")
        print(f"   Length: {len(initial_image_url)} characters")
        
        # Now edit the generated image using EditImageAgent
        print("\n" + "=" * 60)
        print("STEP 2: Editing the generated image...")
        print("=" * 60)
        
        edit_message = {
            "image_url": initial_image_url,
            "prompt": "A few more people were sitting drinking coffee and talking."
        }
        
        print(f"Edit request: {edit_message}")
        
        edit_result = await edit_agent.process_message(
            user_id="test-user",
            session_id="test-session",
            message=str(edit_message).replace("'", '"')  # Convert to proper JSON
        )
        
        print("\n" + "=" * 60)
        print("STEP 3: Results")
        print("=" * 60)
        
        if edit_result["type"] == "image":
            edited_image_url = edit_result['metadata']['image_url']
            original_url = edit_result['metadata'].get('original_url', 'Not provided')
            
            print(f"✅ Image edited successfully!")
            print(f"   Original URL: {original_url}")
            print(f"   Edited URL:   {edited_image_url}")
            print(f"   Style applied: {edit_result['metadata'].get('style', 'N/A')}")
            
            # Check if URLs are actually different
            if initial_image_url == edited_image_url:
                print("⚠️  WARNING: Original and edited URLs are the same!")
                print("   This suggests the editing process may not have worked correctly.")
            else:
                print("✅ URLs are different - edit appears successful!")
                
            # Show URL comparison
            print(f"\nURL Comparison:")
            print(f"  Original length: {len(initial_image_url)}")
            print(f"  Edited length:   {len(edited_image_url)}")
            print(f"  Are they equal?  {initial_image_url == edited_image_url}")
            
        else:
            print(f"❌ Error occurred during editing:")
            print(f"   Type: {edit_result['type']}")
            print(f"   Response: {edit_result['response']}")
            if 'metadata' in edit_result and 'error' in edit_result['metadata']:
                print(f"   Error details: {edit_result['metadata']['error']}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print(f"\n" + "=" * 60)
        print("CLEANUP")
        print("=" * 60)
        await gen_agent.cleanup()
        await edit_agent.cleanup()
        print("✅ Cleanup completed")

if __name__ == "__main__":
    asyncio.run(test_image_edit())
