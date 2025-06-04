from typing import Dict, Any, TypedDict, Literal
from langgraph.graph import Graph, START, END
from models.stt_models import SpeechToTextModel
from .workflow_nodes import WorkflowNode, NodeType

class SpeechState(TypedDict):
    audio_url: str
    text: str
    language: str
    confidence: float
    result: Dict[str, Any]
    next: Literal["transcribe", "validate", "end"]

class SpeechWorkflow:
    """Workflow for speech-to-text processing"""
    
    def __init__(self, speech_model: SpeechToTextModel):
        self.speech_model = speech_model
        self.graph = None
        
    def create_graph(self) -> Graph:
        """Build speech processing workflow"""
        # Create nodes
        transcribe_node = WorkflowNode(self.transcribe_audio, NodeType.VALIDATION)
        
        # Create graph
        workflow = Graph()
        
        # Add nodes
        workflow.add_node("transcribe", transcribe_node)
        
        # Define edges
        workflow.add_edge(START, "transcribe")
        workflow.add_edge("transcribe", END)
        
        self.graph = workflow.compile()
        return self.graph
        
    async def transcribe_audio(self, state: SpeechState) -> SpeechState:
        """Transcribe audio to text"""
        result = await self.speech_model.transcribe(state["audio_url"])
        
        state.update({
            "text": result["text"],
            "language": result["language"],
            "confidence": 1.0,
            "result": result,
            "next": "end"
        })
        
        return state
        
    async def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run speech workflow"""
        if not self.graph:
            self.graph = self.create_graph()
            
        state: SpeechState = {
            "audio_url": config["audio_url"],
            "text": "",
            "language": "",
            "confidence": 0.0,
            "result": {},
            "next": "transcribe"
        }
        
        return await self.graph.ainvoke(state)
