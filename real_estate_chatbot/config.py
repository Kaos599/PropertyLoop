"""
Configuration module for the Real Estate Chatbot.
Loads environment variables and provides configuration functions.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.utilities import GoogleSearchAPIWrapper

# Load environment variables from .env file
load_dotenv()

def get_gemini_flash_llm():
    """
    Returns a configured ChatGoogleGenerativeAI instance using the gemini-2.0-flash model.
    Used primarily for image analysis and routing.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.2,
        convert_system_message_to_human=True
    )

def get_gemini_pro_llm():
    """
    Returns a configured ChatGoogleGenerativeAI instance using the gemini-2.0-flash-thinking-exp-01-21 model.
    Used primarily for text-based analysis and responses.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-thinking-exp-01-21",
        google_api_key=api_key,
        temperature=0.3,
        convert_system_message_to_human=True
    )

def get_google_search():
    """
    Returns a configured GoogleSearchAPIWrapper instance.
    Used for grounding Agent 2 in current tenancy law information.
    
    Note: Not needed when using direct Google genai client with Google Search tool.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return GoogleSearchAPIWrapper(
        google_api_key=api_key
    )

def get_langsmith_client():
    """
    Returns a LangSmith client configuration if credentials are available.
    Optional for tracing and debugging.
    """
    langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
    
    if not langsmith_api_key:
        return None
    
    # LangSmith is configured via environment variables, no client needs to be returned
    return True
