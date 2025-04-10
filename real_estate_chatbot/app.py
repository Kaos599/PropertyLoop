"""
Streamlit application for the Real Estate Chatbot.
Provides a user interface for interacting with the multi-agent system.
"""
import streamlit as st
from PIL import Image
import io
from typing import Dict, List, Any
import base64

from graph import compiled_graph
from schemas import PropertyIssueReport

# Set page configuration
st.set_page_config(
    page_title="Real Estate Assistant",
    page_icon="🏠",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.assistant {
        background-color: #e6f7ff;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .content {
        width: 80%;
    }
    .chat-message .message {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Add title and description
st.title("🏠 Real Estate Assistant")
st.markdown("""
This assistant can help with:
- Identifying property issues from images
- Answering questions about tenancy laws and regulations
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "report" in message:
            # Format PropertyIssueReport in a structured way
            report = message["report"]
            st.markdown("### Property Issue Assessment")
            st.markdown(report.issue_assessment)
            
            if report.troubleshooting_suggestions:
                st.markdown("### Troubleshooting Suggestions")
                for i, suggestion in enumerate(report.troubleshooting_suggestions, 1):
                    st.markdown(f"{i}. {suggestion}")
            
            if report.professional_referral:
                st.markdown("### Professional Referrals")
                for i, referral in enumerate(report.professional_referral, 1):
                    st.markdown(f"{i}. {referral}")
            
            if report.safety_warnings:
                st.markdown("### ⚠️ Safety Warnings")
                for i, warning in enumerate(report.safety_warnings, 1):
                    st.markdown(f"{i}. {warning}")
        else:
            # Regular text message
            st.markdown(message["content"])

# Sidebar for additional context
with st.sidebar:
    st.header("Additional Context")
    location = st.text_input("Location (City/Country for location-specific advice):", key="location")
    st.markdown("---")
    st.markdown("### How to use this chatbot")
    st.markdown("""
    - **For property issues**: Upload an image and describe the issue
    - **For tenancy questions**: Just type your question
    - Provide location for region-specific advice
    """)

# User input area
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Text input
        user_input = st.chat_input("Type your question here...")
    
    with col2:
        # Image upload
        uploaded_file = st.file_uploader("Upload an image of the property issue", type=["jpg", "jpeg", "png"])

# When a user submits input
if user_input or uploaded_file:
    # Prepare image data if uploaded
    image_data = None
    if uploaded_file is not None:
        # Read the file into bytes
        image_bytes = uploaded_file.getvalue()
        image_data = image_bytes
        
        # Display the user's image in the chat
        with st.chat_message("user"):
            st.markdown(user_input if user_input else "")
            st.image(image_bytes, caption="Uploaded Image", use_column_width=True)
        
        # Add to session state with the image
        image_b64 = base64.b64encode(image_bytes).decode()
        if user_input:
            message_content = f"{user_input}\n\n[Image attached]"
        else:
            message_content = "[Image attached]"
        st.session_state.messages.append({"role": "user", "content": message_content, "image": image_b64})
    else:
        # Text-only message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show a spinner while processing
    with st.spinner("Thinking..."):
        # Prepare initial state for the graph
        initial_state = {
            "query": user_input if user_input else "",
            "image_data": image_data,
            "location": None,  # Could be extracted from user input if needed
            "response": None,
            "sender": "user",
            "chat_history": st.session_state.messages
        }
        
        # Invoke the graph
        try:
            response_state = compiled_graph.invoke(initial_state)
            response = response_state["response"]
            
            # Display the response
            with st.chat_message("assistant"):
                if isinstance(response, PropertyIssueReport):
                    # For Agent 1 (Property Issue Detection)
                    st.markdown("### Property Issue Assessment")
                    st.markdown(response.issue_assessment)
                    
                    if response.troubleshooting_suggestions:
                        st.markdown("### Troubleshooting Suggestions")
                        for i, suggestion in enumerate(response.troubleshooting_suggestions, 1):
                            st.markdown(f"{i}. {suggestion}")
                    
                    if response.professional_referral:
                        st.markdown("### Professional Referrals")
                        for i, referral in enumerate(response.professional_referral, 1):
                            st.markdown(f"{i}. {referral}")
                    
                    if response.safety_warnings:
                        st.markdown("### ⚠️ Safety Warnings")
                        for i, warning in enumerate(response.safety_warnings, 1):
                            st.markdown(f"{i}. {warning}")
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": "I've analyzed your property issue.", 
                        "report": response
                    })
                else:
                    # For Agent 2 (Tenancy FAQ) or clarification messages
                    st.markdown(response)
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
        
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"I encountered an error: {str(e)}"
            })

# Footer
st.markdown("---")
st.caption("Real Estate Assistant powered by Langchain, LangGraph, and Google Gemini")
