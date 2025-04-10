"""
LangGraph implementation for the real estate chatbot.
Defines the state, nodes, and edges for the agent workflow.
"""
from typing import Dict, List, Any, TypedDict, Optional, Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END

import agents

# Define the state schema
class ChatState(TypedDict):
    """State for the real estate chatbot graph."""
    query: Optional[str]  # User's text query
    image_data: Optional[bytes]  # Binary image data if uploaded
    location: Optional[str]  # Optional location context
    response: Optional[Any]  # Response to show the user
    sender: str  # Which agent sent the response
    next: Optional[str]  # Next node to route to (for router)
    chat_history: List[Dict[str, str]]  # Chat history for context

# Initialize the graph
def create_graph():
    """
    Creates and returns the compiled LangGraph for the real estate chatbot.
    """
    # Create a new graph
    graph = StateGraph(ChatState)
    
    # Add nodes for each agent function
    graph.add_node("router", agents.route_query)
    graph.add_node("agent_1", agents.run_agent_1)
    graph.add_node("agent_2", agents.run_agent_2)
    graph.add_node("clarification", agents.ask_clarification)
    
    # Define conditional edges from router
    graph.add_conditional_edges(
        "router",
        # This function determines the next node based on router output
        lambda state: state["next"],
        {
            "agent_1": "agent_1",
            "agent_2": "agent_2",
            "clarification": "clarification"
        }
    )
    
    # Connect agent nodes to END
    graph.add_edge("agent_1", END)
    graph.add_edge("agent_2", END)
    graph.add_edge("clarification", END)  # User will provide clarification in next turn
    
    # Set the entry point
    graph.set_entry_point("router")
    
    # Compile the graph
    return graph.compile()

# Create compiled graph instance
compiled_graph = create_graph()
