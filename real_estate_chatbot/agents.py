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

# Import Google's genai client for direct API access
from google import genai
from google.genai import types

import config
from schemas import PropertyIssueReport

# System prompts
PROPERTY_ISSUE_SYSTEM_PROMPT = """
# System Prompt: Property Issue Detection Assistant

You are a Property Issue Detection Assistant, an AI system designed to help users identify problems with their properties through image analysis and provide actionable troubleshooting advice.

## Core Capabilities
- Analyze user-uploaded images of properties to identify visible issues and concerns based on the image AND any accompanying text from the user.
- Generate detailed assessments of detected problems according to the required output schema.
- Provide practical troubleshooting suggestions and remediation advice within the schema.
- Ask clarifying questions ONLY IF the image is completely ambiguous or crucial details are missing AND cannot be inferred. Focus on providing an assessment based on what IS visible first.

## Issue Detection Guidelines
Carefully examine images for common property issues including: Moisture Issues (water damage, mold), Structural Issues (cracks, sagging), Electrical Issues (exposed wires, burn marks - visual only), Plumbing Issues (visible leaks, corrosion), Environmental Issues (poor lighting, pests), Cosmetic Issues (peeling paint, damaged fixtures).

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

## Response Format
- Be concise but thorough
- Use clear, non-technical language
- Structure complex answers with bullet points or numbered lists when appropriate
- When providing information about legal matters, include appropriate disclaimers about not being legal advice

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
        
        # Format response for display
        # Create parts of the response separately to avoid backslash issues
        assessment_section = f"## Property Issue Assessment\n{result.issue_assessment}\n\n"
        
        suggestions_section = "## Troubleshooting Suggestions\n"
        if result.troubleshooting_suggestions:
            suggestions_section += "\n".join([f"- {item}" for item in result.troubleshooting_suggestions])
        else:
            suggestions_section += "No troubleshooting suggestions available."
            
        referrals_section = "\n\n## Professional Referrals\n"
        if result.professional_referral:
            referrals_section += "\n".join([f"- {item}" for item in result.professional_referral])
        else:
            referrals_section += "No professional referrals needed."
            
        warnings_section = "\n\n## Safety Warnings\n"
        if result.safety_warnings:
            warnings_section += "\n".join([f"- {item}" for item in result.safety_warnings])
        else:
            warnings_section += "No immediate safety concerns detected."
            
        # Combine all sections
        formatted_response = assessment_section + suggestions_section + referrals_section + warnings_section
        
        return {
            **state,
            "response": formatted_response,
            "sender": "agent_1",
            "structured_response": result
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
    Uses direct Google genai client with Google Search tool.
    
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
            
        # Initialize the Google genai client
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
            
        genai.configure(api_key=api_key)
        client = genai.Client()
        
        # Set up system instruction and user query
        system_instruction = TENANCY_FAQ_SYSTEM_PROMPT
        
        # Create the model configuration with Google Search tool
        model = "gemini-2.0-flash"  # Using newer model
        
        # Format contents with system instruction and user query
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"{system_instruction}\n\nUser question: {full_query}"),
                ],
            ),
        ]
        
        # Configure the Google Search tool
        tools = [
            types.Tool(google_search=types.GoogleSearch())
        ]
        
        # Set up generation config
        generate_content_config = types.GenerateContentConfig(
            tools=tools,
            response_mime_type="text/plain",
        )
        
        # Get response from the model
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                response_text += chunk.text
        
        return {
            **state,
            "response": response_text,
            "sender": "agent_2"
        }
        
    except Exception as e:
        return {
            **state, 
            "response": f"I encountered an error while researching your tenancy question: {str(e)}. Please try again.",
            "sender": "agent_2"
        }

def route_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Router Agent
    
    Determines which specialized agent should handle the query.
    
    Args:
        state: The current state dictionary
            
    Returns:
        Updated state with routing decision
    """
    query = state.get("query", "")
    image_data = state.get("image_data")
    
    # If image is present, route to Agent 1 (Property Issue Detection)
    if image_data is not None:
        return {**state, "next": "agent_1"}
    
    # For text-only queries, use an LLM to classify
    if query:
        llm = config.get_gemini_flash_llm()
        
        human_message = HumanMessage(content=query)
        system_message = SystemMessage(content=ROUTER_SYSTEM_PROMPT)
        
        # Get classification from the LLM
        response = llm.invoke([system_message, human_message])
        classification = response.content.strip()
        
        if "PROPERTY_ISSUE" in classification:
            # Need image for property issue
            return {**state, "next": "clarification"}
        elif "TENANCY_FAQ" in classification:
            return {**state, "next": "agent_2"}
            
    # Default to clarification for unclear queries or empty queries
    return {**state, "next": "clarification"}

def ask_clarification(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clarification Agent
    
    Asks the user for clarification when the query is unclear.
    
    Args:
        state: The current state dictionary
            
    Returns:
        Updated state with clarification question
    """
    query = state.get("query", "")
    
    # Check if this is likely a property issue question
    if query:
        llm = config.get_gemini_flash_llm()
        human_message = HumanMessage(content=query)
        system_message = SystemMessage(content=ROUTER_SYSTEM_PROMPT)
        
        # Get classification from the LLM
        response = llm.invoke([system_message, human_message])
        classification = response.content.strip()
        
        if "PROPERTY_ISSUE" in classification:
            return {
                **state,
                "response": "To help you with property issues, I'll need to see an image of the problem. Could you please upload a photo?",
                "sender": "clarification"
            }
    
    return {
        **state,
        "response": "I'm not sure what you're asking about. Are you inquiring about property issues (please provide an image) or do you have questions about tenancy laws and regulations?",
        "sender": "clarification"
    }
