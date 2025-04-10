# Real Estate Assistant Chatbot

## Overview
This multi-agent chatbot system is designed to help users with property issues and tenancy questions. The system incorporates image analysis and text-based responses to provide comprehensive real estate assistance.

## Features
- **Property Issue Detection Agent**: Analyzes uploaded images to identify property issues (mold, cracks, leaks, etc.) and provides troubleshooting suggestions
- **Tenancy FAQ Agent**: Answers questions about tenant rights, landlord responsibilities, and rental regulations with location-specific guidance
- **Smart Routing**: Automatically determines which agent should handle each query based on input type

## Technology Stack
- **Orchestration**: Langchain & LangGraph
- **LLMs**: Google Gemini (gemini-1.5-flash-latest, gemini-1.5-pro-latest)
- **Grounding**: Google Search API
- **UI**: Streamlit
- **Configuration**: Python with dotenv
- **Data Validation**: Pydantic

## Setup/Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_google_cse_id
   ```

## Usage
1. Navigate to the project directory
2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
3. Access the web interface at http://localhost:8501
4. For property issues:
   - Upload an image of the property issue
   - Optionally include a description
5. For tenancy questions:
   - Simply type your question (no image needed)

## Configuration
Required environment variables:
- `GOOGLE_API_KEY`: API key for Google Gemini and Google Search
- `GOOGLE_CSE_ID`: Custom Search Engine ID for Google Search

Optional environment variables:
- `LANGCHAIN_TRACING_V2`: Enable LangSmith tracing
- `LANGCHAIN_ENDPOINT`: LangSmith endpoint URL
- `LANGCHAIN_API_KEY`: LangSmith API key
- `LANGCHAIN_PROJECT`: LangSmith project name

## Project Structure
- `.env`: Environment variables for API keys
- `config.py`: Configuration module
- `schemas.py`: Pydantic schemas for structured output
- `agents.py`: Implements Agent 1 and Agent 2 logic
- `graph.py`: LangGraph state definition and workflow
- `app.py`: Streamlit web application
- `requirements.txt`: Project dependencies
