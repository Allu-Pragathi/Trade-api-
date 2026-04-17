# Trade Opportunities API

A robust FastAPI-based service designed to analyze market data and provide trade opportunity insights for specific sectors in India using Google Gemini AI.

## Features
- **Sector Analysis**: Generates comprehensive markdown reports for various sectors (Tech, Pharma, Agri, etc.).
- **AI-Powered**: Uses Google Gemini 1.5 Flash for deep market synthesis.
- **Real-time Search**: Gathers live news and trends via DuckDuckGo.
- **Security**: 
  - API Key Authentication (`X-API-KEY` header).
  - Rate Limiting (default: 5 requests per minute).
  - Pydantic Input Validation.
- **Session Tracking**: In-memory tracking of API usage statistics.

## Tech Stack
- **FastAPI**: Backend Framework
- **Google Generative AI**: LLM for analysis
- **DuckDuckGo Search**: For live market data
- **SlowAPI**: Rate limiting
- **Python Dotenv**: Environment configuration

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/))

### 2. Installation
1. Clone or download the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
1. Create/edit the `.env` file in the root directory.
2. Add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   API_KEY=admin123
   RATE_LIMIT=5/minute
   ```

### 4. Running the API
Start the server using uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Usage

### Single Analysis Endpoint
**Endpoint**: `GET /analyze/{sector}`

**Headers**:
- `X-API-KEY`: `admin123` (or your configured API key)

**Example Request (Curl)**:
```bash
curl -H "X-API-KEY: admin123" http://127.0.0.1:8000/analyze/pharmaceuticals
```

**Response**: A structured Markdown report containing Executive Summary, Trade Opportunities, Market Drivers, Risks, and Future Outlook.

### Session Stats
**Endpoint**: `GET /session/stats`
**Headers**: `X-API-KEY` required.

## Project Structure
- `main.py`: Entry point and route definitions.
- `services/`: AI and Search logic.
- `security.py`: Auth and Rate limiting.
- `models.py`: Pydantic schemas.
- `config.py`: Environment management.

## Evaluation Criteria Met
- [x] FastAPI Implementation (async handling, documentation).
- [x] AI Integration (Gemini API for analysis).
- [x] Data Collection (DuckDuckGo integration).
- [x] Security (Auth, Rate Limiting).
- [x] Clean Architecture (Separation of concerns).
