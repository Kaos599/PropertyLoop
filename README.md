# PropertyLoop Real Estate Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.18-green)](https://github.com/langchain-ai/langchain)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Gemini](https://img.shields.io/badge/Gemini_AI-2.0-orange)](https://ai.google.dev/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/Kaos599/PropertyLoop)
[![Demo](https://img.shields.io/badge/Demo-Live-success)](https://property-loop-assistant.streamlit.app/)

A sophisticated AI-powered real estate assistant built to serve landlords, property managers, and tenants with accurate, personalized, and contextually relevant information about property management, tenancy law, and maintenance issues.

[![Video Title](https://img.youtube.com/vi/8tDXYwhQdkY/0.jpg)](https://www.youtube.com/watch?v=8tDXYwhQdkY)

## Features

### 🏠 Multi-Agent Architecture
- **Specialized Agent System**: Leverages multiple AI agents, each with distinct expertise areas including property issues, legal matters, and tenancy FAQs
- **Collaborative Problem Solving**: Agents work together through a directed knowledge graph to provide comprehensive responses
- **Advanced Context Management**: Maintains conversation history to provide consistent, personalized responses

### 📋 Property Issue Reporting
- **Detailed Problem Documentation**: Capture, categorize, and evaluate property maintenance issues
- **Severity Assessment**: AI-driven evaluation of issue urgency and potential impact
- **Solution Recommendations**: Practical guidance for addressing common property problems
- **Professional Referral**: Suggestions for when to contact qualified professionals
- **Image Analysis**: Upload and analyze property images to identify issues visually

### ⚖️ Legal & Regulatory Guidance
- **Tenancy Law Information**: Clear explanations of rights and responsibilities
- **Region-Specific Advice**: Location-aware recommendations based on local regulations
- **Contract Interpretation**: Help understanding lease agreements and rental terms
- **Compliance Guidance**: Information on safety regulations and legal requirements

### 💬 Natural Conversation Interface
- **Context-Aware Responses**: Understands complex questions and provides relevant answers
- **Multimedia Support**: Upload images of property issues for enhanced analysis
- **Location Awareness**: Provides region-specific advice when location is specified
- **User-Friendly Design**: Intuitive interface with premium enterprise SaaS aesthetic
- **Conversation Memory**: Maintains context across multiple messages for natural conversations
- **Reference Tracking**: Intelligently tracks previous discussions to provide coherent follow-up responses

### 🔍 Advanced Information Retrieval
- **Knowledge Integration**: Combines specialized property management knowledge with broader real estate information
- **Citation Support**: References reliable sources for legal and regulatory information
- **Up-to-date Information**: Access to current best practices and regulations

### 🔄 Enhanced Conversation Context
- **Intelligent Context Extraction**: Maintains conversation flow by extracting and using relevant information from previous messages
- **Image Context Management**: Properly integrates image analysis results into conversational context
- **Property Details Integration**: Incorporates property information (type, age, location) into responses
- **Conversation Continuity**: Follows up on previously discussed issues with appropriate context

### 🛡️ Error Handling & Reliability
- **Robust Error Prevention**: Advanced error handling for uninterrupted user experience
- **Reliable Image Processing**: Ensures images are processed only once and properly analyzed
- **Graceful Degradation**: Maintains functionality even when certain data is missing or incomplete
- **Safe Message Processing**: Protects against issues with unexpected message formats or content

## Technical Overview

### Architecture
The system uses a directed knowledge graph implemented with LangGraph to coordinate specialized agents:

1. **Router Agent**: Directs queries to appropriate specialist agents
2. **Property Issues Agent**: Handles maintenance and property problem questions
3. **Legal Agent**: Provides regulatory and compliance information
4. **Tenancy FAQ Agent**: Answers common questions about tenancy agreements and processes
5. **Safety Agent**: Addresses urgent safety concerns with appropriate warnings

### Context Management System
The application implements sophisticated context management through:

1. **Historical Message Analysis**: Intelligently extracts relevant information from previous interactions
2. **Context-Aware Queries**: Enhances user queries with appropriate historical context
3. **Message Type Handling**: Properly processes different types of messages (text, images, structured responses)
4. **Error-Resistant Processing**: Handles missing or malformed data gracefully

### Technologies Used
- **LangChain & LangGraph**: For agent orchestration and knowledge management
- **Generative AI**: Powered by advanced language models for natural conversations
- **Streamlit**: For the responsive web interface
- **Python**: Core programming language with data processing capabilities
- **Pydantic**: For structured data validation and schema enforcement

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip package manager

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Kaos599/property-loop-real-estate-chatbot.git
cd property-loop-real-estate-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with:
```
GOOGLE_API_KEY=your_google_api_key
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage Examples

### Property Issue Reporting
Ask about specific property problems:
> "There's a water leak under my kitchen sink. What should I do?"

Upload an image of the issue for better analysis:
> [Upload image] "What's wrong with this wall and how can I fix it?"

### Follow-up Questions
The chatbot maintains context for natural follow-ups:
> "How much would it cost to repair?"
> "Is this something I can do myself?"

### Tenancy Questions
Inquire about common rental situations:
> "My landlord wants to increase my rent. How much notice should they give me?"

### Legal Guidance
Get information about regulations:
> "What are the legal requirements for carbon monoxide detectors in a rental property?"

### Regional Specifics
Get location-aware advice:
> "What are the eviction notice requirements in London?"

## Advanced Features

### Context Management
The system maintains conversation context across multiple interactions, allowing for natural follow-up questions without repeating information. For example:

1. Ask about a property issue
2. Upload an image of the issue
3. Ask follow-up questions about repair costs, DIY options, or professional services
4. The chatbot remembers the context and provides coherent responses

### Error Handling
The application gracefully handles various types of errors:

- Missing or malformed data
- Interrupted operations
- Image processing failures
- Connectivity issues

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- The LangChain and Streamlit communities for their excellent tools
