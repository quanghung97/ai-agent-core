from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from config.settings import get_settings
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger(__name__)

class DallEModel:
    """Wrapper for DALL-E API with enhanced features"""
    
    def __init__(self):
        self.settings = get_settings()
        if not self.settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in settings")
            
        self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.supported_models = {
            "generate": ["dall-e-2", "dall-e-3"],
            "edit": ["dall-e-2"]  # Only dall-e-2 supports editing
        }
        self.quality_options = ["standard", "hd"]
        self.size_options = {
            "dall-e-2": ["256x256", "512x512", "1024x1024"],
            "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"]
        }

    async def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "hd",
        style: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate image with enhanced options"""
        if model not in self.supported_models["generate"]:
            raise ValueError(f"Unsupported model: {model}")
        
        if size not in self.size_options[model]:
            raise ValueError(f"Invalid size for {model}: {size}")

        try:
            # Add style to prompt if specified
            full_prompt = f"{prompt}, {style}" if style else prompt
            
            response = await self.client.images.generate(
                model=model,
                prompt=full_prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="url"
            )

            print(f"DALL-E generation response: {response}")

            return {
                "url": response.data[0].url,
                "model": model,
                "size": size,
                "quality": quality,
                "style": style,
                "created": response.created
            }
        except Exception as e:
            raise Exception(f"DALL-E generation failed: {str(e)}")

    async def _download_image(self, url: str) -> bytes:
        """Download image from URL and return as bytes"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download image: HTTP {response.status}")
                    return await response.read()
        except Exception as e:
            logger.error(f"Image download failed: {str(e)}")
            raise

    async def _convert_to_png_bytes(self, image_data: bytes) -> bytes:
        """Convert image data to PNG format and return as bytes"""
        try:
            # Open image with PIL
            image = Image.open(BytesIO(image_data))
            
            # Convert to RGBA if not already (ensures compatibility)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Save to BytesIO buffer as PNG
            png_buffer = BytesIO()
            image.save(png_buffer, format='PNG')
            png_buffer.seek(0)
            
            return png_buffer.getvalue()
                
        except Exception as e:
            logger.error(f"Image conversion failed: {str(e)}")
            raise

    async def edit_image(
        self,
        image_url: str,
        prompt: str,
    ) -> Dict[str, Any]:
        """Edit existing image with DALL-E using auto-generated mask"""
        try:
            print(f"Starting DALL-E edit process...")
            print(f"  Image URL: {image_url}")
            print(f"  Prompt: {prompt}")
            
            # Download and convert main image to PNG
            image_data = await self._download_image(image_url)
            png_image_data = await self._convert_to_png_bytes(image_data)

            # Create file object for OpenAI
            image_file = BytesIO(png_image_data)
            image_file.name = 'image.png'
            
            # Create BytesIO objects for the API
            print("  Calling DALL-E edit API...")
            response = await self.client.images.edit(
                image=image_file,
                prompt=prompt,
                model="dall-e-2",  # Only dall-e-2 supports editing
                n=1,               # number of images to generate
                size="1024x1024",  # dall-e-2 edit only supports 1024x1024
                response_format="url"
            )
            
            new_url = response.data[0].url
            print(f"  New image URL: {new_url}")
            
            return {
                "url": new_url,
                "model": "dall-e-2",
                "created": response.created,
                "edited": True,
            }
            
        except Exception as e:
            logger.error(f"DALL-E image editing failed: {str(e)}")
            raise Exception(f"DALL-E image editing failed: {str(e)}")

