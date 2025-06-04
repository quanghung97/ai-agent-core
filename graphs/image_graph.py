from typing import Dict, Any, TypedDict, Literal
from langgraph.graph import Graph, START, END
from models.dalle_models import DallEModel
from personality.personality_config import PersonalityConfig

class ImageState(TypedDict):
    prompt: str
    image_url: str
    size: str
    model: str
    quality: str
    style: str | None
    result: Dict[str, Any]
    operation: Literal["generate", "edit"]
    next: str

class ImageWorkflow:
    """LangGraph workflow for image operations with personality"""
    
    def __init__(self, dalle_model: DallEModel, personality: PersonalityConfig):
        self.dalle_model = dalle_model
        self.personality = personality
        self.graph = None
        self.edit_graph = None
        
    def create_graph(self) -> Graph:
        """Build graph for image generation"""
        # Create new graph with async config
        workflow = Graph()
        
        # Add nodes
        workflow.add_node("enhance", self.enhance_prompt)
        workflow.add_node("generate", self.generate_image)
        workflow.add_node("process", self.post_process)
        
        # Define workflow
        workflow.add_edge(START, "enhance")
        workflow.add_edge("enhance", "generate")
        workflow.add_edge("generate", "process")
        workflow.add_edge("process", END)
        
        # Compile the graph
        self.graph = workflow.compile()
        return self.graph
    
    async def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run image generation workflow"""
        if not self.graph:
            self.graph = self.create_graph()
            print("Graph created for image generation")
        state: ImageState = {
            "prompt": config["prompt"],
            "image_url": "",
            "size": config.get("size", "1024x1024"),
            "model": config.get("model", "dall-e-3"),
            "quality": config.get("quality", "hd"),
            "style": config.get("style"),
            "result": {},
            "operation": "generate",
            "next": "enhance"
        }
        
        return await self.graph.ainvoke(state)

    def create_edit_graph(self) -> Graph:
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
        self.edit_graph = workflow.compile()
        return self.edit_graph

    async def run_edit(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run image editing workflow"""
        if not self.edit_graph:
            self.edit_graph = self.create_edit_graph()
            
        state: ImageState = {
            "prompt": config["prompt"],
            "image_url": config["image_url"],
            "size": "1024x1024",  # DALL-E edit only supports 1024x1024
            "model": "dall-e-2",   # Only DALL-E 2 supports editing
            "quality": "standard",  # DALL-E 2 doesn't support "hd" quality
            "style": self.personality.artistic_style,
            "result": {},
            "operation": "edit",
            "next": "enhance"
        }
        
        return await self.edit_graph.ainvoke(state)

    async def enhance_prompt(self, state: ImageState) -> ImageState:
        """Enhance prompt with personality traits"""
        base_prompt = state["prompt"]
        
        # Add artistic style based on personality
        if self.personality.artistic_style:
            base_prompt += f", {self.personality.artistic_style}"
            
        # Add quality enhancements based on personality traits
        if self.personality.personality_traits.detail_oriented > 0.7:
            base_prompt += ", highly detailed, intricate"
        
        if self.personality.personality_traits.creativity > 0.7:
            base_prompt += ", creative and imaginative"
            
        state["prompt"] = base_prompt
        
        return state

    async def generate_image(self, state: ImageState) -> ImageState:
        """Generate image with enhanced prompt"""
        print("Generating image with state:", state)
        result = await self.dalle_model.generate_image(
            prompt=state["prompt"],
            model=state["model"],
            size=state["size"],
            quality=state["quality"],
            style=state["style"]
        )
        print("111", result)
        state["image_url"] = result["url"]
        state["result"] = result
        return state

    async def edit_image(self, state: ImageState) -> ImageState:
        """Edit image with enhanced prompt"""
        result = await self.dalle_model.edit_image(
            image_url=state["image_url"],
            prompt=state["prompt"]
        )
        state["image_url"] = result["url"]
        state["result"] = result
        return state

    async def post_process(self, state: ImageState) -> ImageState:
        """Post-process the generated image"""
        state["result"].update({
            "personality_influence": {
                "artistic_style": self.personality.artistic_style,
                "creativity": self.personality.personality_traits.creativity,
                "detail_oriented": self.personality.personality_traits.detail_oriented
            }
        })
        return state
