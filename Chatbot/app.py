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
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from graph import compiled_graph
from schemas import PropertyIssueReport, TenancyFAQResponse

# Set page configuration
st.set_page_config(
    page_title="PropertyLoop Assistant",
    page_icon="🏠",
    layout="wide"
)

# Updated premium enterprise SaaS dark theme with 8px grid system
st.markdown("""
<style>
    /* Base Variables - 8px Grid System with Premium Color Palette */
    :root {
        /* Primary Colors */
        --primary-dark: #0F172A;
        --primary-main: #1E293B;
        --primary-light: #334155;
        --primary-accent: #0D9488;
        
        /* Secondary Colors */
        --secondary-warm: #F59E0B;
        --secondary-slate: #64748B;
        --secondary-slate-light: #94A3B8;
        
        /* State Colors */
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --info: #3B82F6;
        
        /* Text Colors */
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --text-tertiary: #94A3B8;
        
        /* Spacing - 8px Grid */
        --space-1: 8px;
        --space-2: 16px;
        --space-3: 24px;
        --space-4: 32px;
        --space-5: 40px;
        --space-6: 48px;
        
        /* Typography Scale */
        --text-xs: 12px;
        --text-sm: 14px;
        --text-base: 16px;
        --text-lg: 20px;
        --text-xl: 24px;
        --text-2xl: 32px;
        
        /* Z-Depth Levels */
        --z-depth-0: none;
        --z-depth-1: 0 2px 4px rgba(0, 0, 0, 0.1);
        --z-depth-2: 0 4px 8px rgba(0, 0, 0, 0.12);
        --z-depth-3: 0 8px 16px rgba(0, 0, 0, 0.14);
        --z-depth-4: 0 12px 24px rgba(0, 0, 0, 0.16);
        --z-depth-8: 0 24px 48px rgba(0, 0, 0, 0.24);
        
        /* Transitions */
        --transition-fast: all 0.2s ease;
        --transition-medium: all 0.3s ease;
        --transition-slow: all 0.5s ease;
        
        /* Borders */
        --border-radius-sm: 4px;
        --border-radius-md: 8px;
        --border-radius-lg: 16px;
        --border-width: 1px;
    }

    /* Global Styles */
    body {
        background-color: var(--primary-dark);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.5;
        font-size: var(--text-base);
    }

    .stApp {
        background-color: var(--primary-dark);
    }

    /* Main Content Area */
    .main > div {
        padding: 0 var(--space-3);
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Typography Hierarchy */
    h1 {
        font-size: var(--text-2xl) !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        margin-bottom: var(--space-2) !important;
        color: var(--text-primary) !important;
    }

    h2 {
        font-size: var(--text-xl) !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        margin-bottom: var(--space-2) !important;
        color: var(--primary-accent) !important;
    }

    h3 {
        font-size: var(--text-lg) !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        margin-bottom: var(--space-1) !important;
        color: var (--text-primary) !important;
    }

    p {
        font-size: var(--text-base);
        line-height: 1.6;
        margin-bottom: var(--space-2);
        color: var(--text-secondary);
    }

    /* Premium Card Component Styles */
    .premium-card {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-dark));
        border: var(--border-width) solid rgba(255, 255, 255, 0.08);
        border-radius: var(--border-radius-lg);
        padding: var(--space-3);
        margin-bottom: var(--space-3);
        box-shadow: var(--z-depth-2), inset 0 1px 2px rgba(255, 255, 255, 0.05);
        transition: var(--transition-medium);
        position: relative;
        overflow: hidden;
    }

    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--z-depth-3), inset 0 1px 3px rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.12);
    }
    
    .premium-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-accent), var(--secondary-warm));
        opacity: 0.8;
    }

    .agent-card {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-light));
        border: var(--border-width) solid rgba(255, 255, 255, 0.08);
        border-radius: var(--border-radius-lg);
        padding: var(--space-3);
        margin-bottom: var(--space-3);
        box-shadow: var(--z-depth-2), inset 0 1px 2px rgba(255, 255, 255, 0.05);
        transition: var(--transition-medium);
        position: relative;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--z-depth-3), inset 0 1px 3px rgba(255, 255, 255, 0.08);
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: var(--primary-accent);
    }

    .agent-title {
        color: var(--primary-accent) !important;
        font-size: var(--text-lg);
        font-weight: 600;
        margin-bottom: var(--space-2);
        display: flex;
        align-items: center;
        gap: var(--space-1);
    }

    .agent-title svg {
        width: 20px;
        height: 20px;
    }

    /* Chat Message Styling */
    .chat-message {
        border-radius: var(--border-radius-lg);
        margin: var(--space-3) 0;
        padding: var(--space-3);
        box-shadow: var(--z-depth-2);
        transition: var(--transition-fast);
        position: relative;
        overflow: hidden;
    }

    .chat-message:hover {
        box-shadow: var(--z-depth-3);
    }

    .chat-message.user {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-light));
        border-left: 4px solid var(--secondary-warm);
        margin-left: var(--space-4);
        margin-right: 0;
    }

    .chat-message.assistant {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-dark));
        border-left: 4px solid var(--primary-accent);
        margin-right: var(--space-4);
        margin-left: 0;
    }

    /* Streamlit default chat message overrides */
    .stChatMessage {
        margin: var(--space-3) 0 !important;
    }

    .stChatMessage > div {
        padding: 0 !important;
    }

    .stChatMessage [data-testid="chatAvatarIcon-user"],
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        top: var(--space-1) !important;
    }

    /* Main Header Styling */
    .main-header {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-dark));
        border-radius: var(--border-radius-lg);
        padding: var(--space-4);
        margin: var(--space-3) 0;
        border: var(--border-width) solid rgba(255, 255, 255, 0.08);
        box-shadow: var(--z-depth-2), inset 0 1px 2px rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-accent), var(--secondary-warm));
        opacity: 0.8;
    }

    .main-header h1 {
        color: var(--primary-accent) !important;
        font-size: var(--text-2xl);
        margin-bottom: var(--space-1);
        font-weight: 700;
    }

    .main-header p {
        color: var(--text-secondary);
        font-size: var(--text-lg);
        margin-bottom: 0;
    }

    /* Response Cards */
    .property-issue,
    .professional-referral,
    .safety-warning,
    .tenancy-answer,
    .legal-references,
    .regional-specifics,
    .disclaimer,
    .resources,
    .troubleshooting {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-light));
        border-radius: var(--border-radius-md);
        padding: var(--space-3);
        margin-bottom: var (--space-3);
        box-shadow: var(--z-depth-1);
        position: relative;
        border-left-width: 4px;
        border-left-style: solid;
    }

    .property-issue {
        border-left-color: var(--primary-accent);
    }

    .professional-referral {
        border-left-color: var(--info);
    }

    .safety-warning {
        border-left-color: var(--error);
    }

    .tenancy-answer {
        border-left-color: var(--primary-accent);
    }

    .legal-references {
        border-left-color: var(--info);
    }

    .regional-specifics {
        border-left-color: var(--success);
    }

    .disclaimer {
        border-left-color: var(--warning);
        font-size: var(--text-sm);
    }

    .resources {
        border-left-color: var(--secondary-warm);
    }

    .troubleshooting {
        border-left-color: var(--success);
    }

    /* Form Controls */
    .stButton button {
        background: linear-gradient(145deg, var(--primary-accent), #0B7C72) !important;
        color: white !important;
        border-radius: var(--border-radius-md);
        font-weight: 600;
        padding: var(--space-1) var(--space-3) !important;
        border: none !important;
        box-shadow: var(--z-depth-1);
        transition: var(--transition-fast);
        text-transform: uppercase;
        font-size: var(--text-sm);
        letter-spacing: 0.5px;
        width: 100%;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: var(--z-depth-2);
        background: linear-gradient(145deg, #0E9E92, var(--primary-accent)) !important;
    }

    .stButton button:active {
        transform: translateY(0);
    }

    .stTextInput input, .stTextArea textarea {
        background: var(--primary-main) !important;
        color: var(--text-primary) !important;
        border: var(--border-width) solid rgba(255, 255, 255, 0.1) !important;
        border-radius: var (--border-radius-md) !important;
        padding: var(--space-2) !important;
        box-shadow: var(--z-depth-0), inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        transition: var(--transition-fast) !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary-accent) !important;
        box-shadow: 0 0 0 1px var(--primary-accent), inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    .stSelectbox > div > div {
        background: var(--primary-main) !important;
        border: var(--border-width) solid rgba(255, 255, 255, 0.1) !important;
        border-radius: var(--border-radius-md) !important;
    }

    .stSelectbox > div > div:hover {
        border-color: var(--primary-accent) !important;
    }

    /* Radio buttons and checkboxes */
    .stRadio label {
        color: var(--text-primary) !important;
        font-size: var(--text-base);
        padding: var(--space-1) 0;
    }

    .stRadio [role="radiogroup"] {
        padding: var(--space-1) 0;
    }

    /* Sliders */
    .stSlider [data-baseweb="slider"] {
        margin-top: var(--space-2) !important;
    }

    .stSlider .st-c7 {
        background: var(--primary-accent) !important;
    }
    
    .stSlider [data-testid="stThumbValue"] {
        background: var(--primary-accent) !important;
        color: white !important;
    }

    /* Location Status */
    .location-applied {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-light));
        border-radius: var(--border-radius-md);
        border: var(--border-width) solid rgba(255, 255, 255, 0.08);
        padding: var(--space-2);
        display: flex;
        align-items: center;
        gap: var(--space-1);
        margin-top: var(--space-2);
        font-size: var(--text-sm);
    }

    .location-applied-icon {
        color: var(--success);
        font-weight: bold;
    }

    /* Image Upload Area */
    .image-preview {
        border: 2px dashed rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius-lg);
        background: var(--primary-main);
        padding: var(--space-2);
        margin-top: var(--space-2);
        transition: var(--transition-fast);
        overflow: hidden;
    }

    .image-preview:hover {
        border-color: var(--primary-accent);
    }
    
    .image-preview img {
        border-radius: var(--border-radius-md);
        box-shadow: var(--z-depth-1);
    }

    /* File uploader enhancements */
    .stFileUploader > div {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-dark)) !important;
        border-radius: var(--border-radius-md) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        padding: var(--space-2) !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* Sidebar Styling */
    .stSidebar {
        background: var(--primary-main) !important;
        border-right: var(--border-width) solid rgba(255, 255, 255, 0.05);
    }
    
    .stSidebar [data-testid="stSidebar"] {
        width: 320px !important;
    }

    .stSidebar .stMarkdown h3 {
        font-size: var(--text-lg) !important;
        color: var(--primary-accent) !important;
        margin-top: var(--space-3) !important;
        padding-bottom: var(--space-1);
        border-bottom: var(--border-width) solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar section separation */
    .stSidebar > div > div > div > div:not(:first-child) {
        margin-top: var(--space-3);
        padding-top: var(--space-3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Footer */
    .footer {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-dark));
        border-top: var(--border-width) solid rgba(255, 255, 255, 0.05);
        padding: var(--space-3);
        margin-top: var(--space-4);
        border-radius: var(--border-radius-md);
        font-size: var(--text-sm);
        color: var(--text-tertiary);
        text-align: center;
    }

    .footer strong {
        color: var(--text-secondary);
    }

    /* Code Blocks */
    code {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-light)) !important;
        color: var(--primary-accent) !important;
        padding: 2px 6px !important;
        border-radius: var(--border-radius-sm) !important;
        font-size: var(--text-sm) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Markdown Content */
    .stMarkdown p {
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: var(--text-base);
    }

    .stMarkdown strong {
        color: var(--text-primary);
        font-weight: 600;
    }

    .stMarkdown ul, .stMarkdown ol {
        margin-left: var(--space-3);
        margin-bottom: var(--space-3);
    }

    .stMarkdown li {
        margin-bottom: var(--space-1);
        color: var(--text-secondary);
    }

    /* Make the chat input more prominent */
    .stChatInput {
        padding-top: var(--space-1) !important;
        border-top: var(--border-width) solid rgba(255, 255, 255, 0.05);
        margin: var(--space-3) 0 !important;
    }

    .stChatInput > div {
        background: linear-gradient(145deg, var(--primary-main), var(--primary-light)) !important;
        border-radius: var(--border-radius-lg) !important;
        padding: var(--space-1) !important;
        border: var(--border-width) solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: var(--z-depth-2) !important;
    }

    .stChatInput input {
        background: transparent !important;
        color: var(--text-primary) !important;
        padding: var(--space-2) !important;
        font-size: var(--text-base) !important;
    }

    /* Fix for the black box behind chat input */
    .stChatInput div[data-baseweb="input"] {
        background-color: transparent !important;
    }
    
    .stChatInput [data-testid="stChatInputContainer"] {
        background-color: transparent !important;
    }
    
    /* Override Streamlit chat input container backgrounds */
    /* This specifically targets the black box behind the chat input */
    .stChatInput div[data-baseweb="input"] {
        background-color: transparent !important;
    }
    
    .stChatInput [data-testid="stChatInputContainer"] {
        background-color: transparent !important;
    }
    
    /* Also target the input element itself to ensure it's transparent */
    .stChatInput div[data-baseweb="input"] > div {
        background-color: transparent !important;
    }
    
    /* Target any potential nested divs that might have background color */
    .stChatInput div[data-baseweb="input"] div {
        background-color: transparent !important;
    }
    
    /* Important fix for the black background box */
    .stChatInput div:has(>div[data-baseweb="input"]) {
        background-color: transparent !important;
    }
    
    /* Final catch-all for any deeply nested elements */
    .stChatInput * {
        background-color: transparent !important;
    }

    .stChatInput button svg {
        color: var(--primary-accent) !important;
    }

    /* Spinner Styling */
    .stSpinner > div {
        border-color: var(--primary-accent) transparent var(--primary-accent) transparent !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        color: var(--text-primary) !important;
        background: linear-gradient(145deg, var(--primary-main), var (--primary-light)) !important;
        border-radius: var(--border-radius-md) !important;
        padding: var(--space-2) var(--space-3) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(145deg, var(--primary-light), var(--primary-main)) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 0 0 var(--border-radius-md) var(--border-radius-md) !important;
        padding: var(--space-2) !important;
    }

    /* Custom Z-depth classes for optional use */
    .z-depth-0 { box-shadow: var(--z-depth-0); }
    .z-depth-1 { box-shadow: var(--z-depth-1); }
    .z-depth-2 { box-shadow: var(--z-depth-2); }
    .z-depth-3 { box-shadow: var(--z-depth-3); }
    .z-depth-4 { box-shadow: var(--z-depth-4); }
    .z-depth-8 { box-shadow: var(--z-depth-8); }
    
    /* Responsive adjustments */
    @media screen and (max-width: 768px) {
        :root {
            --text-xs: 10px;
            --text-sm: 12px;
            --text-base: 14px;
            --text-lg: 18px;
            --text-xl: 20px;
            --text-2xl: 24px;
            
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 16px;
            --space-4: 24px;
            --space-5: 32px;
            --space-6: 40px;
        }
        
        .main > div {
            padding: 0 var(--space-2);
        }
        
        .chat-message.user {
            margin-left: var(--space-2);
        }
        
        .chat-message.assistant {
            margin-right: var(--space-2);
        }
        
        .main-header {
            padding: var(--space-3);
        }
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
    
    # Location input with confirmation indicator
    if "location_set" not in st.session_state:
        st.session_state.location_set = False
    
    # Location input with autocomplete suggestions
    popular_locations = ["London, UK", "New York, USA", "Sydney, Australia", "Toronto, Canada", "Berlin, Germany"]
    location = st.text_input("Location (City/Country):", key="location", 
                            placeholder="E.g. London, UK",
                            on_change=lambda: setattr(st.session_state, 'location_set', bool(st.session_state.location)))
    
    # Show confirmation if location is set
    if st.session_state.location_set and st.session_state.location:
        st.markdown(f'<div class="location-applied"><span class="location-applied-icon">✓</span> Location set to: {st.session_state.location}</div>', unsafe_allow_html=True)
    
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
        st.session_state.location_set = False
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a variable to track if chat input should be disabled during processing
if "is_chat_input_disabled" not in st.session_state:
    st.session_state.is_chat_input_disabled = False

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
                    st.markdown('<div class="troubleshooting">', unsafe_allow_html=True)
                    for i, suggestion in enumerate(report.troubleshooting_suggestions, 1):
                        st.markdown(f"{i}. {suggestion}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
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
user_input = st.chat_input("Type your question here...", disabled=st.session_state.is_chat_input_disabled)

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
    
    # Disable chat input during processing
    st.session_state.is_chat_input_disabled = True
    
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
        
        # Add debug logging for tenancy questions
        if user_input and not uploaded_file:
            # Check if input looks like a tenancy question
            tenancy_keywords = ["tenant", "landlord", "rent", "lease", "notice", "deposit", "eviction", 
                               "contract", "tenancy", "agreement", "property manager", "vacate"]
            
            is_likely_tenancy = any(keyword in user_input.lower() for keyword in tenancy_keywords)
            logger.debug(f"Query: {user_input}")
            logger.debug(f"Is likely tenancy question: {is_likely_tenancy}")
            logger.debug(f"Context string: {context_str}")
            
            # Force tenancy mode for common tenancy questions
            if "notice" in user_input.lower() and "vacate" in user_input.lower():
                logger.debug("Detected notice to vacate question - forcing tenancy mode")
                # Add a hint to the query to help the model recognize this as a tenancy question
                enhanced_query = f"[TENANCY QUESTION] {enhanced_query}"
        
        # Prepare initial state for the graph
        initial_state = {
            "query": enhanced_query,
            "image_data": image_data,
            "location": context_info["location"],
            "response": None,
            "sender": "user",
            "chat_history": st.session_state.messages
        }
        
        logger.debug(f"Initial state: {initial_state}")
        
        # Invoke the graph
        try:
            logger.debug("Invoking agent graph...")
            response_state = compiled_graph.invoke(initial_state)
            response = response_state["response"]
            logger.debug(f"Response type: {type(response)}")
            logger.debug(f"Response content: {response}")
            
            # Debug log full response state
            for key, value in response_state.items():
                if key != "chat_history" and key != "image_data":  # Skip large data
                    logger.debug(f"Response state - {key}: {value}")
            
            # Display the response
            with st.chat_message("assistant", avatar="🏠"):
                if isinstance(response, PropertyIssueReport):
                    logger.debug("Rendering PropertyIssueReport")
                    st.markdown("### Property Issue Assessment")
                    st.markdown(f'<div class="property-issue">{response.issue_assessment}</div>', unsafe_allow_html=True)
                    
                    if response.troubleshooting_suggestions:
                        st.markdown("### Troubleshooting Suggestions")
                        st.markdown('<div class="troubleshooting">', unsafe_allow_html=True)
                        for i, suggestion in enumerate(response.troubleshooting_suggestions, 1):
                            st.markdown(f"{i}. {suggestion}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
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
                    logger.debug("Rendering TenancyFAQResponse")
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
                    logger.debug(f"Rendering plain text response: {response}")
                    st.markdown(response)
                    # Add to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
        
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            st.error(f"Error processing request: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"I encountered an error: {str(e)}"
            })
    
    # Re-enable chat input after processing
    st.session_state.is_chat_input_disabled = False

# Footer with attribution
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("**PropertyLoop Assignment by Harsh Dayal**")
st.markdown("Email: harshdayal13@gmail.com")
st.markdown(f"© {datetime.datetime.now().year} PropertyLoop Assistant powered by Langchain, LangGraph, and Google Gemini")
st.markdown('</div>', unsafe_allow_html=True)
