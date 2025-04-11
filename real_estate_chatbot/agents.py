"""
Implementation of the agents for the real estate chatbot.
Contains the logic for the property issue detection agent, tenancy FAQ, and router.
"""
from typing import Dict, List, Any, Optional, Tuple
import base64
import os
from io import BytesIO
from PIL import Image

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# Import Google's generative AI client
import google.generativeai as genai
from google.generativeai import types

import config
from schemas import PropertyIssueReport, TenancyFAQResponse

# System prompts
PROPERTY_ISSUE_SYSTEM_PROMPT = """
# System Prompt: Property Issue Detection Assistant

You are a Property Issue Detection Assistant, an AI system designed to help users identify problems with their properties through image analysis and provide actionable troubleshooting advice.

## Core Capabilities
- Analyze user-uploaded images of properties to identify visible issues and concerns based on the image AND any accompanying text from the user.
- Generate detailed assessments of detected problems according to the required output schema.
- Provide practical troubleshooting suggestions and remediation advice within the schema.
- Consider additional context like property type, age, and occupancy status if provided.
- Ask clarifying questions ONLY IF the image is completely ambiguous or crucial details are missing AND cannot be inferred. Focus on providing an assessment based on what IS visible first.

## Issue Detection Guidelines
Carefully examine images for common property issues including: 
- Moisture Issues (water damage, mold, damp patches)
- Structural Issues (cracks, sagging, foundation problems, subsidence)
- Electrical Issues (exposed wires, burn marks, outdated wiring - visual only)
- Plumbing Issues (visible leaks, corrosion, water stains, discoloration)
- Environmental Issues (poor lighting, pests, ventilation problems)
- Cosmetic Issues (peeling paint, damaged fixtures, worn-out materials)

## Response Format REQUIRED
You **MUST** respond using the structured output format defined by the `PropertyIssueReport` Pydantic schema. Populate the following fields based on your analysis:
1.  **issue_assessment**: Clear, detailed description of identified problems. If multiple, list them. If none detected, state that clearly.
2.  **troubleshooting_suggestions**: Specific, actionable advice for each issue. Link suggestions to the assessments.
3.  **professional_referral**: Recommendations for professionals (Plumber, Electrician, etc.) relevant to the identified issues.
4.  **safety_warnings**: Urgent warnings for potential hazards (electrical risks, structural concerns, health hazards from mold). If none, this can be an empty list.

## Communication Guidelines
- Use clear, accessible language.
- Be thorough but concise.
- Prioritize analysis of visible evidence in the image and user text.
- If property details (type, age, occupancy) are provided, incorporate this into your analysis.

## Response Limitations
- Base assessment solely on visible evidence. State if an issue needs in-person professional inspection for confirmation.
- Do not guess or provide information not supported by visual evidence.
"""

TENANCY_FAQ_SYSTEM_PROMPT = """
# System Prompt: Tenancy Law and FAQ Assistant

You are a Tenancy FAQ Assistant, specialized in answering questions about property rentals, tenant-landlord relationships, and housing regulations. 

## Core Capabilities
- Answer questions about tenant rights, landlord responsibilities, and property rental procedures
- Provide location-specific guidance when a location is mentioned in the query
- Ground your answers in factual information by performing web searches for legal or regulatory information
- Deliver clear, practical advice to help users navigate tenancy situations

## Guidelines for Responses
- Always search for up-to-date information when answering questions about specific laws, regulations, or location-specific practices
- Clearly indicate when information may vary by jurisdiction if no specific location is provided
- Be balanced in representing both tenant and landlord perspectives
- Provide actionable next steps when appropriate
- Cite sources of information when possible

## Response Format REQUIRED
You **MUST** respond using the structured output format defined by the `TenancyFAQResponse` Pydantic schema. Populate the following fields based on your analysis:
1. **answer**: Your main response to the user's tenancy-related question. Be direct, informative, and helpful.
2. **legal_references**: List relevant laws, regulations, or legal principles you've referenced. Include specific acts, statutes, or regulations when possible.
3. **regional_specifics**: If a location was provided, include location-specific information here. Otherwise, leave as null.
4. **disclaimer**: The default legal disclaimer will be included automatically.
5. **additional_resources**: List organizations, websites, or other resources the user can contact for more information.

## Communication Guidelines
- Use clear, non-technical language
- Structure complex answers with bullet points or numbered lists when appropriate
- When providing information about legal matters, maintain a balanced perspective
- Base your answers on current, accurate information from reliable sources

Remember to search for current information before answering questions about specific tenancy laws or regulations, especially when a location is specified.
"""

ROUTER_SYSTEM_PROMPT = """
You are a routing agent for a real estate assistance system. Your job is to analyze the user query and determine which specialized agent should handle it.

If the query includes an image or mentions analyzing a photo/picture of a property issue, route to Agent 1 (Property Issue Detection).

If the query is about tenancy laws, tenant rights, landlord obligations, lease agreements, or any rental/housing regulations, route to Agent 2 (Tenancy FAQ).

If the query is unclear or doesn't fit either category, respond with "UNCLEAR_ISSUE".

Respond only with one of these exact labels: "PROPERTY_ISSUE", "TENANCY_FAQ", or "UNCLEAR_ISSUE".
"""

def run_agent_1(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 1: Property Issue Detection Agent
    
    Analyzes images of property issues and provides structured assessment and advice.
    
    Args:
        state: The current state dictionary containing:
            - query: The user's text query
            - image_data: The binary image data
            
    Returns:
        Updated state with response added
    """
    try:
        query = state.get("query", "")
        image_data = state.get("image_data")
        
        if not image_data:
            return {
                **state,
                "response": "I need an image to analyze property issues. Please upload a photo of the issue.",
                "sender": "agent_1"
            }
        
        # Process the image data
        # Convert bytes to base64 for Gemini
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        image_uri = f"data:image/jpeg;base64,{encoded_image}"
        
        # Extract additional context if available
        context = []
        if "location" in state and state["location"]:
            context.append(f"Location: {state['location']}")
            
        # Create multimodal input for Gemini
        human_message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": query if query else "Please analyze this image for property issues."
                },
                {
                    "type": "image_url",
                    "image_url": image_uri
                }
            ]
        )
        
        # Initialize the LLM
        llm = config.get_gemini_flash_llm()
        
        # Run inference with structured output
        result = llm.with_structured_output(PropertyIssueReport).invoke(
            [
                SystemMessage(content=PROPERTY_ISSUE_SYSTEM_PROMPT),
                human_message
            ]
        )
        
        # Return the structured output directly to be handled by the UI
        return {
            **state,
            "response": result,
            "sender": "agent_1"
        }
        
    except Exception as e:
        return {
            **state,
            "response": f"I encountered an error analyzing the image: {str(e)}. Please try again with a clearer image.",
            "sender": "agent_1"
        }

def run_agent_2(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 2: Tenancy FAQ Agent
    
    Answers questions about tenancy laws and regulations with grounding via Google Search.
    Uses direct Google genai client with Google Search tool and returns structured output.
    
    Args:
        state: The current state dictionary containing:
            - query: The user's text query
            - location: Optional location context
            
    Returns:
        Updated state with response added
    """
    try:
        query = state.get("query", "")
        location = state.get("location", "")
        
        if not query:
            return {
                **state,
                "response": "I need a question about tenancy or rental properties to assist you.",
                "sender": "agent_2"
            }
        
        # Format query with location if available
        if location:
            full_query = f"{query} (Location: {location})"
        else:
            full_query = query
            
        # Use the LangChain wrapper for Google Gemini instead of direct client
        llm = config.get_gemini_pro_llm()
        
        # Create a prompt that includes instructions for web search
        search_prompt = f"""
{TENANCY_FAQ_SYSTEM_PROMPT}

User question: {full_query}

Before answering:
1. Perform a web search to find current information about this tenancy question
2. If location-specific information is available, prioritize that
3. Cite your sources in the legal_references field
"""
        
        # Create messages for the LLM
        messages = [
            SystemMessage(content=search_prompt)
        ]
        
        # Run inference with structured output
        result = llm.with_structured_output(TenancyFAQResponse).invoke(messages)
        
        # Return the structured output directly to be handled by the UI
        return {
            **state,
            "response": result,
            "sender": "agent_2"
        }
        
    except Exception as e:
        return {
            **state,
            "response": f"I encountered an error answering your question: {str(e)}. Please try rephrasing or asking a different question.",
            "sender": "agent_2"
        }

def route_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Router to determine which agent should handle the query.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with next node to route to
    """
    try:
        query = state.get("query", "")
        image_data = state.get("image_data")
        
        # If there's an image, definitely route to Agent 1
        if image_data:
            return {
                **state,
                "next": "agent_1"
            }
        
        # If no query, ask for clarification
        if not query.strip():
            return {
                **state,
                "next": "clarification",
                "response": "Please provide a question or upload an image of a property issue so I can assist you."
            }
        
        # Initialize the LLM
        llm = config.get_gemini_flash_llm()
        
        # Get routing decision
        router_response = llm.invoke(
            [
                SystemMessage(content=ROUTER_SYSTEM_PROMPT),
                HumanMessage(content=query)
            ]
        )
        
        router_decision = router_response.content.strip()
        
        if "PROPERTY_ISSUE" in router_decision:
            if not image_data:
                return {
                    **state,
                    "next": "clarification",
                    "response": "It looks like you're asking about a property issue. Could you upload an image of the issue so I can analyze it better?"
                }
            else:
                return {
                    **state,
                    "next": "agent_1"
                }
        elif "TENANCY_FAQ" in router_decision:
            return {
                **state,
                "next": "agent_2"
            }
        else:  # UNCLEAR_ISSUE
            return {
                **state,
                "next": "clarification",
                "response": "I'm not sure if you're asking about a property issue or a tenancy question. Could you provide more details or specify which type of assistance you need?"
            }
    
    except Exception as e:
        return {
            **state,
            "next": "clarification",
            "response": f"I encountered an error routing your query: {str(e)}. Could you please rephrase your question?"
        }

def ask_clarification(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Asks for clarification when query is unclear.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with clarification response
    """
    # If response is already set by router, use that
    if "response" in state and state["response"]:
        return {
            **state,
            "sender": "clarification"
        }
    
    # Default clarification message
    return {
        **state,
        "response": "I need more information to help you. Are you asking about a property issue (please upload an image if so) or do you have a question about tenancy laws and regulations?",
        "sender": "clarification"
    }
