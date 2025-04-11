"""
Streamlit application for the Real Estate Chatbot.
Provides a user interface for interacting with the multi-agent system.
"""
import streamlit as st
from PIL import Image
import io
from typing import Dict, List, Any
import base64
import datetime

from graph import compiled_graph
from schemas import PropertyIssueReport, TenancyFAQResponse

# Set page configuration
st.set_page_config(
    page_title="PropertyLoop Assistant",
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
    .main-header {
        background-color: #4a6fa5;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .sub-header {
        color: #4a6fa5;
        margin-bottom: 1rem;
    }
    .agent-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .agent-title {
        font-weight: bold;
        color: #4a6fa5;
    }
    .property-issue {
        background-color: #f0f7ff;
        border-left: 5px solid #4a90e2;
        padding: 1rem;
        border-radius: 5px;
    }
    .professional-referral {
        background-color: #fff0f0;
        border-left: 5px solid #e24a4a;
        padding: 1rem;
        border-radius: 5px;
    }
    .safety-warning {
        background-color: #fff9e0;
        border-left: 5px solid #e2c94a;
        padding: 1rem;
        border-radius: 5px;
    }
    .stButton button {
        background-color: #4a6fa5;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f5f5f5;
        border-radius: 10px;
    }
    .image-preview {
        border: 1px dashed #cccccc;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
    }
    .custom-tabs .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .custom-tabs .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .custom-tabs .stTabs [aria-selected="true"] {
        background-color: #4a6fa5;
        color: white;
    }
    .tenancy-answer {
        background-color: #f0f7ff;
        border-left: 5px solid #4a90e2;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .legal-references {
        background-color: #f0f0f7;
        border-left: 5px solid #7a4ae2;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .regional-specifics {
        background-color: #e6f7e6;
        border-left: 5px solid #4ae24a;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .disclaimer {
        background-color: #f7f7f0;
        border-left: 5px solid #e2c94a;
        padding: 1rem;
        border-radius: 5px;
        font-size: 0.9em;
        font-style: italic;
        margin-bottom: 1rem;
    }
    .resources {
        background-color: #f7f0f7;
        border-left: 5px solid #e24a9a;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Add title and description
st.markdown('<div class="main-header"><h1>🏠 PropertyLoop Assistant</h1><p>Your virtual real estate consultant</p></div>', unsafe_allow_html=True)

# Two-column layout for agent description
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="agent-card"><p class="agent-title">🔍 Agent 1: Issue Detection & Troubleshooting</p><p>Upload property images to identify issues like water damage, mold, cracks, broken fixtures, etc. Get troubleshooting advice and professional recommendations.</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="agent-card"><p class="agent-title">📜 Agent 2: Tenancy FAQ</p><p>Get answers about tenancy laws, agreements, landlord/tenant responsibilities, and rental processes. Provide your location for region-specific guidance.</p></div>', unsafe_allow_html=True)

# Sidebar for additional context
with st.sidebar:
    st.header("Additional Context")
    
    # Location input with autocomplete suggestions
    popular_locations = ["London, UK", "New York, USA", "Sydney, Australia", "Toronto, Canada", "Berlin, Germany"]
    location = st.text_input("Location (City/Country):", key="location", 
                            placeholder="E.g. London, UK")
    
    # Property type selection
    st.subheader("Property Details")
    property_type = st.selectbox(
        "Property Type:",
        ["Apartment/Flat", "House", "Condo", "Studio", "Commercial", "Other"],
        index=0
    )
    
    # Occupancy status
    occupancy = st.radio(
        "Occupancy Status:",
        ["Owner-occupied", "Tenant-occupied", "Vacant", "Not applicable"]
    )
    
    # Property age slider
    property_age = st.slider("Property Age (years):", 0, 100, 10)
    
    st.markdown("---")
    
    # Upload image section with preview
    st.subheader("Property Image")
    uploaded_file = st.file_uploader("Upload an image of the property issue", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(uploaded_file, caption="Image Preview", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### How to use this chatbot")
    st.markdown("""
    - **For property issues**: Upload an image and describe the issue
    - **For tenancy questions**: Just type your question
    - Provide location for region-specific advice
    """)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
            if "image" in message:
                # Display image if it exists in the message
                image_data = base64.b64decode(message["image"])
                st.image(image_data, caption="Uploaded Image", use_column_width=True)
    else:  # assistant message
        with st.chat_message("assistant", avatar="🏠"):
            if "property_report" in message:
                # Format PropertyIssueReport in a structured way
                report = message["property_report"]
                
                st.markdown(f"### Property Issue Assessment")
                st.markdown(f'<div class="property-issue">{report.issue_assessment}</div>', unsafe_allow_html=True)
                
                if report.troubleshooting_suggestions:
                    st.markdown("### Troubleshooting Suggestions")
                    for i, suggestion in enumerate(report.troubleshooting_suggestions, 1):
                        st.markdown(f"{i}. {suggestion}")
                
                if report.professional_referral:
                    st.markdown("### Professional Referrals")
                    st.markdown('<div class="professional-referral">', unsafe_allow_html=True)
                    for i, referral in enumerate(report.professional_referral, 1):
                        st.markdown(f"{i}. {referral}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if report.safety_warnings:
                    st.markdown("### ⚠️ Safety Warnings")
                    st.markdown('<div class="safety-warning">', unsafe_allow_html=True)
                    for i, warning in enumerate(report.safety_warnings, 1):
                        st.markdown(f"{i}. {warning}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            elif "tenancy_response" in message:
                # Format TenancyFAQResponse in a structured way
                response = message["tenancy_response"]
                
                st.markdown("### Answer")
                st.markdown(f'<div class="tenancy-answer">{response.answer}</div>', unsafe_allow_html=True)
                
                if response.legal_references and len(response.legal_references) > 0:
                    st.markdown("### Legal References")
                    st.markdown('<div class="legal-references">', unsafe_allow_html=True)
                    for i, reference in enumerate(response.legal_references, 1):
                        st.markdown(f"{i}. {reference}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if response.regional_specifics:
                    st.markdown("### Regional Information")
                    st.markdown(f'<div class="regional-specifics">{response.regional_specifics}</div>', unsafe_allow_html=True)
                
                if response.additional_resources and len(response.additional_resources) > 0:
                    st.markdown("### Additional Resources")
                    st.markdown('<div class="resources">', unsafe_allow_html=True)
                    for i, resource in enumerate(response.additional_resources, 1):
                        st.markdown(f"{i}. {resource}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="disclaimer">{response.disclaimer}</div>', unsafe_allow_html=True)
                
            else:
                # Regular text message
                st.markdown(message["content"])

# User input area
user_input = st.chat_input("Type your question here...")

# When a user submits input
if user_input or (uploaded_file and 'last_file' not in st.session_state or uploaded_file != st.session_state.get('last_file')):
    if uploaded_file:
        st.session_state.last_file = uploaded_file
        
    # Prepare image data if uploaded
    image_data = None
    if uploaded_file is not None:
        # Read the file into bytes
        image_bytes = uploaded_file.getvalue()
        image_data = image_bytes
        
        # Display the user's image in the chat
        with st.chat_message("user", avatar="👤"):
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
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show a spinner while processing
    with st.spinner("Processing your request..."):
        # Get additional context from sidebar
        context_info = {
            "location": st.session_state.location if hasattr(st.session_state, 'location') and st.session_state.location else None,
            "property_type": property_type,
            "occupancy": occupancy,
            "property_age": property_age
        }
        
        # Format context for query
        context_str = ""
        if context_info["location"]:
            context_str += f" Location: {context_info['location']}."
        if context_info["property_type"] != "Other":
            context_str += f" Property type: {context_info['property_type']}."
        if context_info["occupancy"] != "Not applicable":
            context_str += f" Occupancy: {context_info['occupancy']}."
        if context_info["property_age"] > 0:
            context_str += f" Property age: {context_info['property_age']} years."
        
        # Append context to query if it exists
        enhanced_query = user_input if user_input else ""
        if context_str and enhanced_query:
            enhanced_query += f"\n\nAdditional context:{context_str}"
        
        # Prepare initial state for the graph
        initial_state = {
            "query": enhanced_query,
            "image_data": image_data,
            "location": context_info["location"],
            "response": None,
            "sender": "user",
            "chat_history": st.session_state.messages
        }
        
        # Invoke the graph
        try:
            response_state = compiled_graph.invoke(initial_state)
            response = response_state["response"]
            
            # Display the response
            with st.chat_message("assistant", avatar="🏠"):
                if isinstance(response, PropertyIssueReport):
                    # For Agent 1 (Property Issue Detection)
                    st.markdown("### Property Issue Assessment")
                    st.markdown(f'<div class="property-issue">{response.issue_assessment}</div>', unsafe_allow_html=True)
                    
                    if response.troubleshooting_suggestions:
                        st.markdown("### Troubleshooting Suggestions")
                        for i, suggestion in enumerate(response.troubleshooting_suggestions, 1):
                            st.markdown(f"{i}. {suggestion}")
                    
                    if response.professional_referral:
                        st.markdown("### Professional Referrals")
                        st.markdown('<div class="professional-referral">', unsafe_allow_html=True)
                        for i, referral in enumerate(response.professional_referral, 1):
                            st.markdown(f"{i}. {referral}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    if response.safety_warnings:
                        st.markdown("### ⚠️ Safety Warnings")
                        st.markdown('<div class="safety-warning">', unsafe_allow_html=True)
                        for i, warning in enumerate(response.safety_warnings, 1):
                            st.markdown(f"{i}. {warning}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": "I've analyzed your property issue.", 
                        "property_report": response
                    })
                
                elif isinstance(response, TenancyFAQResponse):
                    # For Agent 2 (Tenancy FAQ)
                    st.markdown("### Answer")
                    st.markdown(f'<div class="tenancy-answer">{response.answer}</div>', unsafe_allow_html=True)
                    
                    if response.legal_references and len(response.legal_references) > 0:
                        st.markdown("### Legal References")
                        st.markdown('<div class="legal-references">', unsafe_allow_html=True)
                        for i, reference in enumerate(response.legal_references, 1):
                            st.markdown(f"{i}. {reference}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    if response.regional_specifics:
                        st.markdown("### Regional Information")
                        st.markdown(f'<div class="regional-specifics">{response.regional_specifics}</div>', unsafe_allow_html=True)
                    
                    if response.additional_resources and len(response.additional_resources) > 0:
                        st.markdown("### Additional Resources")
                        st.markdown('<div class="resources">', unsafe_allow_html=True)
                        for i, resource in enumerate(response.additional_resources, 1):
                            st.markdown(f"{i}. {resource}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="disclaimer">{response.disclaimer}</div>', unsafe_allow_html=True)
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": "I've answered your tenancy question.", 
                        "tenancy_response": response
                    })
                
                else:
                    # For other types of messages (like clarification)
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

# Footer with attribution
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("**PropertyLoop Assignment by Harsh Dayal**")
st.markdown("Email: harshdayal13@gmail.com")
st.markdown(f"© {datetime.datetime.now().year} PropertyLoop Assistant powered by Langchain, LangGraph, and Google Gemini")
st.markdown('</div>', unsafe_allow_html=True)
