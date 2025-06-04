from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from models.dalle_models import DallEModel
from graphs.image_graph import ImageWorkflow
from personality.personality_config import PersonalityConfig
import logging
import json

logger = logging.getLogger(__name__)

class ImageAgent(BaseAgent):
    """Agent for handling image generation and editing with personality"""

    def __init__(self, agent_id: str, personality: PersonalityConfig):
        super().__init__(agent_id)
        self.personality = personality
        self.dalle_model = DallEModel()
        self.workflow = ImageWorkflow(self.dalle_model, self.personality)
        self.graph = self.workflow.create_graph()

    async def initialize(self) -> None:
        """Initialize agent resources"""
        pass

    async def process_message(
        self,
        user_id: str,
        message: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process image generation/editing requests from messages"""
        try:
            # Parse message content
            request = self._parse_image_request(message)
            
            result = await self.generate_image(
                prompt=request["prompt"],
                size=request.get("size", "1024x1024"),
                model=request.get("model", "dall-e-3"),
                style=request.get("style"),
                quality=request.get("quality", "hd")
            )

            return {
                "response": "Image generated successfully",
                "session_id": session_id,
                "user_id": user_id,
                "type": "image",
                "metadata": {
                    "image_url": result.get("image_url"),
                    "model": result.get("model"),
                    "size": result.get("size"),
                    "style": result.get("style")
                }
            }
            
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            return {
                "response": f"Failed to process image request: {str(e)}",
                "session_id": session_id,
                "user_id": user_id,
                "type": "error",
                "metadata": {"error": str(e)}
            }

    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        self.graph = None
        self.edit_graph = None
        
    def _parse_image_request(self, message: str) -> Dict[str, Any]:
        """Parse message into image request parameters"""
        try:
            # Check if message is JSON
            if message.strip().startswith('{'):
                return json.loads(message)
            
            # Default to generate operation with message as prompt
            return {
                "operation": "generate",
                "prompt": message,
                "style": self.personality.artistic_style
            }
        except json.JSONDecodeError:
            return {
                "operation": "generate",
                "prompt": message,
                "style": self.personality.artistic_style
            }

    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        model: str = "dall-e-3",
        style: Optional[str] = None,
        quality: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate image with personality-enhanced prompts"""
        try:   
            result = await self.workflow.run({
                "prompt": prompt,
                "size": size,
                "model": model,
                "style": style or self.personality.artistic_style,
                "quality": quality or "hd"
            })
            return result
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise
