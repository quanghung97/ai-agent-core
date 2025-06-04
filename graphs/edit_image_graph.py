from typing import Dict, Any, TypedDict
from langgraph.graph import Graph, START, END
from models.dalle_models import DallEModel
from personality.personality_config import PersonalityConfig

class EditImageState(TypedDict):
    prompt: str
    image_url: str
    original_url: str  # Keep track of original URL
    style: str | None
    result: Dict[str, Any]
    next: str

class EditImageWorkflow:
    """LangGraph workflow for image editing operations"""
    
    def __init__(self, dalle_model: DallEModel, personality: PersonalityConfig):
        self.dalle_model = dalle_model
        self.personality = personality
        self.graph = None
        
    def create_graph(self) -> Graph:
        """Build graph for image editing"""
        workflow = Graph()
        
        # Add nodes for editing
        workflow.add_node("enhance", self.enhance_prompt)
        workflow.add_node("edit", self.edit_image)
        workflow.add_node("process", self.post_process)
        
        # Define workflow
        workflow.add_edge(START, "enhance")
        workflow.add_edge("enhance", "edit")
        workflow.add_edge("edit", "process")
        workflow.add_edge("process", END)
        
        # Compile the graph
        self.graph = workflow.compile()
        return self.graph

    async def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run image editing workflow"""
        if not self.graph:
            self.graph = self.create_graph()
            
        state: EditImageState = {
            "prompt": config["prompt"],
            "image_url": config["image_url"],
            "original_url": config["image_url"],  # Store original URL
            "style": self.personality.artistic_style,
            "result": {},
            "next": "enhance"
        }
        
        # Run the workflow and get the final state
        final_state = await self.graph.ainvoke(state)
        
        # Return the properly structured result
        return {
            "image_url": final_state["image_url"],
            "original_url": final_state["original_url"],
            "result": final_state["result"]
        }

    async def enhance_prompt(self, state: EditImageState) -> EditImageState:
        """Enhance edit prompt with personality traits"""
        base_prompt = state["prompt"]
        
        if self.personality.artistic_style:
            base_prompt += f", {self.personality.artistic_style}"
            
        if self.personality.personality_traits.detail_oriented > 0.7:
            base_prompt += ", maintain high detail and consistency"
        
        if self.personality.personality_traits.creativity > 0.7:
            base_prompt += ", creative and harmonious modifications"
            
        state["prompt"] = base_prompt
        return state

    async def edit_image(self, state: EditImageState) -> EditImageState:
        """Edit image with enhanced prompt"""
        try:
            result = await self.dalle_model.edit_image(
                image_url=state["image_url"],
                prompt=state["prompt"]
            )
            # Update state with the new edited image URL
            state["image_url"] = result["url"]  # This should be the NEW edited image URL
            state["result"] = result
            return state
        except Exception as e:
            # Log the error and re-raise with more context
            print(f"Error in edit_image: {str(e)}")
            raise Exception(f"Failed to edit image: {str(e)}")

    async def post_process(self, state: EditImageState) -> EditImageState:
        """Post-process the edited image"""
        state["result"].update({
            "personality_influence": {
                "artistic_style": self.personality.artistic_style,
                "creativity": self.personality.personality_traits.creativity,
                "detail_oriented": self.personality.personality_traits.detail_oriented
            },
            "original_url": state["original_url"],
            "edited_url": state["image_url"]  # Make sure we track both URLs
        })
        return state
