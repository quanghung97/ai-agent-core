from typing import Dict, Any, List, Literal, TypedDict, Optional
from langgraph.graph import Graph, START, END
from .base_graph import BaseWorkflow
from .workflow_nodes import WorkflowNode, WorkflowNodes, NodeType
from models.openai_models import OpenAIChat
from models.search_models import SearchModel
from personality.personality_config import PersonalityConfig
from utils.error_handling import WorkflowError, with_retry, RetryableError, NodeExecutionError
from memory.knowledge_memory import KnowledgeMemory
import logging

logger = logging.getLogger(__name__)

class ChatState(TypedDict):
    messages: List[Dict[str, str]]
    intent: str
    memory: Dict[str, Any]
    response: Dict[str, Any]
    searched: bool
    search_results: Optional[Dict[str, Any]]
    next: Literal["validate", "classify", "memory", "chat", "search", "end"]

class ChatWorkflow(BaseWorkflow):
    def __init__(self, openai_chat: OpenAIChat, personality: PersonalityConfig, knowledge_memory: KnowledgeMemory):
        super().__init__()
        self.openai_chat = openai_chat
        self.search_model = SearchModel()
        self.personality = personality
        self.knowledge_memory = knowledge_memory
        self.nodes = WorkflowNodes()
        self.graph = None

    def create_graph(self) -> Graph:
        """Create enhanced workflow graph with search capability"""
        # Create nodes
        validate_node = WorkflowNode(self.nodes.validate_input, NodeType.VALIDATION)
        intent_node = WorkflowNode(self.nodes.classify_intent, NodeType.CLASSIFICATION)
        memory_node = WorkflowNode(self.nodes.update_memory, NodeType.MEMORY)
        chat_node = WorkflowNode(self.process_chat, NodeType.CHAT)
        search_node = WorkflowNode(self.process_search, NodeType.SEARCH)        

        # Create graph
        workflow = Graph()
        
        # Add nodes
        workflow.add_node("validate", validate_node)
        workflow.add_node("classify", intent_node)
        workflow.add_node("memory", memory_node)
        workflow.add_node("chat", chat_node)
        workflow.add_node("search", search_node)
        
        # Define edges
        def route_back_to_chat(state: Dict[str, Any]) -> Dict[str, Any]:
            if state["next"] == "search":
                return "search"
            else:
                return END

        workflow.add_edge(START, "validate")
        workflow.add_edge("validate", "classify")
        workflow.add_edge("classify", "memory")
        workflow.add_edge("memory", "chat")
        workflow.add_conditional_edges("chat", route_back_to_chat)
        workflow.add_edge("search", "chat")  # Search can go back to chat
        
        self.graph = workflow.compile()
        return self.graph
    
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run workflow with search capability"""
        if not self.graph:
            self.graph = self.create_graph()
            
        # Initialize state
        workflow_state = {
            "messages": state.get("messages", []),
            "intent": "",
            "memory": {
                "turn_count": 0,
                "topics": [],
                "sentiment": "neutral",
                "last_intent": "",
                "session_data": {}
            },
            "response": {
                "response": "",
                "type": "text",
                "metadata": {}
            },
            "searched": False,
            "search_results": None,
            "next": "validate"
        }
        
        try:
            result = await self.graph.ainvoke(workflow_state)
            return result
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return self.format_error_response(workflow_state, str(e))

    @with_retry(max_retries=2, delay=1.0)
    async def process_chat(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process chat with search capability"""
        try:
            messages = state.get("messages", [])
            print(f"Processing chat with messages: {messages}")
            memory = state.get("memory", {})
            
            # Add system message if not present
            if not any(msg.get("role") == "system" for msg in messages):
                messages.insert(0, {
                    "role": "system",
                    "content": self.personality.generate_prompt()
                })

            # If we have search results, add them to context
            if state.get("search_results"):
                messages.append({
                    "role": "system",
                    "content": f"Here is some additional information: {state['search_results']['content']}"
                })

            # Generate response
            response = await self.openai_chat.generate_response(
                messages=messages,
                temperature=0.7
            )

            # Check if response indicates lack of knowledge
            needs_search = any(phrase in response.lower() for phrase in [
                "i don't know", "i'm not sure", "i cannot", "i don't have",
                "i cannot find", "i cannot answer", "i don't understand"
            ])

            if needs_search and not state.get("searched"):
                # Set state for search
                state["next"] = "search"
                state["searched"] = True
                return state

            # Add response and continue
            messages.append({
                "role": "assistant",
                "content": response
            })

            return {
                "messages": messages,
                "response": {
                    "response": response,
                    "type": "text",
                    "metadata": {
                        "intent": state.get("intent", "general"),
                        "memory": memory,
                        "searched": state.get("searched", False)
                    }
                },
                "memory": memory,
                "searched": state.get("searched", False),
                "search_results": state.get("search_results"),
                "next": "end"
            }

        except Exception as e:
            logger.error(f"Chat processing failed: {str(e)}")
            raise NodeExecutionError(f"Chat processing failed: {str(e)}")

    @with_retry(max_retries=2, delay=1.0)
    async def process_search(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process search using both knowledge base and external search"""
        try:
            last_message = next(
                (msg["content"] for msg in reversed(state["messages"]) 
                 if msg["role"] == "user"),
                None
            )

            if last_message:
                # First, query knowledge base
                knowledge_results = await self.knowledge_memory.query_knowledge(last_message)
                print(f"Knowledge base results: {knowledge_results}")
                
                if knowledge_results and knowledge_results[0]["relevance_score"] > 0.8:
                    # Use knowledge base results if highly relevant
                    state["search_results"] = {
                        "content": knowledge_results[0]["content"],
                        "source": "knowledge_base",
                        "metadata": knowledge_results[0]["metadata"]
                    }
                else:
                    # Fall back to external search
                    search_results = await self.search_model.search(last_message)
                    state["search_results"] = search_results

                state["next"] = "chat"
                return state
            
            state["next"] = "end"
            return state

        except Exception as e:
            logger.error(f"Search processing failed: {str(e)}")
            raise NodeExecutionError(f"Search processing failed: {str(e)}")

