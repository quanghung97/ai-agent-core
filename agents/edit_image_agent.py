from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from models.dalle_models import DallEModel
from graphs.edit_image_graph import EditImageWorkflow
from personality.personality_config import PersonalityConfig
import logging
import json

logger = logging.getLogger(__name__)

class EditImageAgent(BaseAgent):
    """Agent for handling image editing with personality"""

    def __init__(self, agent_id: str, personality: PersonalityConfig):
        super().__init__(agent_id)
        self.personality = personality
        self.dalle_model = DallEModel()
        self.workflow = EditImageWorkflow(self.dalle_model, self.personality)
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
        """Process image editing requests from messages"""
        try:
            request = self._parse_edit_request(message)
            
            print(f"Processing edit request:")
            print(f"  Original URL: {request['image_url']}")
            print(f"  Prompt: {request['prompt']}")
            
            result = await self.edit_image(
                image_url=request["image_url"],
                prompt=request["prompt"]
            )

            print(f"Edit result:")
            print(f"  New URL: {result['image_url']}")
            print(f"  Original URL: {result.get('original_url', 'N/A')}")

            return {
                "response": "Image edited successfully",
                "session_id": session_id,
                "user_id": user_id,
                "type": "image",
                "metadata": {
                    "image_url": result["image_url"],  # This should be the NEW edited image
                    "original_url": request["image_url"],  # This is the original
                    "style": result["result"].get("style"),
                    "edit_details": result["result"]
                }
            }
            
        except Exception as e:
            logger.error(f"Image editing failed: {str(e)}")
            return {
                "response": f"Failed to edit image: {str(e)}",
                "session_id": session_id,
                "user_id": user_id,
                "type": "error",
                "metadata": {"error": str(e)}
            }

    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        self.graph = None
        
    def _parse_edit_request(self, message: str) -> Dict[str, Any]:
        """Parse edit request from message"""
        try:
            if message.strip().startswith('{'):
                data = json.loads(message)
                
                # Validate required fields
                if "image_url" not in data:
                    raise ValueError("Missing required field: image_url")
                if "prompt" not in data:
                    raise ValueError("Missing required field: prompt")
                    
                return data
            
            raise ValueError("Edit requests must be in JSON format")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in edit request: {str(e)}")

    async def edit_image(
        self,
        image_url: str,
        prompt: str
    ) -> Dict[str, Any]:
        """Edit image with personality-influenced modifications"""
        try:
            print(f"Starting image edit workflow...")
            print(f"  Input URL: {image_url}")
            print(f"  Prompt: {prompt}")
            
            result = await self.workflow.run({
                "image_url": image_url,
                "prompt": prompt
            })
            
            print(f"Workflow completed:")
            print(f"  Result URL: {result.get('image_url', 'NO URL')}")
            print(f"  Original URL: {result.get('original_url', 'NO ORIGINAL')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Image editing failed: {str(e)}")
            print(f"Error in edit_image: {str(e)}")
            raise
