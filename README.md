# PropertyLoop Real Estate Assistant

A sophisticated AI-powered real estate assistant built to serve landlords, property managers, and tenants with accurate, personalized, and contextually relevant information about property management, tenancy law, and maintenance issues.

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

### 🔍 Advanced Information Retrieval
- **Knowledge Integration**: Combines specialized property management knowledge with broader real estate information
- **Citation Support**: References reliable sources for legal and regulatory information
- **Up-to-date Information**: Access to current best practices and regulations

## Technical Overview

### Architecture
The system uses a directed knowledge graph implemented with LangGraph to coordinate specialized agents:

1. **Router Agent**: Directs queries to appropriate specialist agents
2. **Property Issues Agent**: Handles maintenance and property problem questions
3. **Legal Agent**: Provides regulatory and compliance information
4. **Tenancy FAQ Agent**: Answers common questions about tenancy agreements and processes
5. **Safety Agent**: Addresses urgent safety concerns with appropriate warnings

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

### Tenancy Questions
Inquire about common rental situations:
> "My landlord wants to increase my rent. How much notice should they give me?"

### Legal Guidance
Get information about regulations:
> "What are the legal requirements for carbon monoxide detectors in a rental property?"

### Regional Specifics
Get location-aware advice:
> "What are the eviction notice requirements in London?"

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- The LangChain and Streamlit communities for their excellent tools
