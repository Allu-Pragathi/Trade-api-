import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    API_KEY = os.getenv("API_KEY", "admin123")
    RATE_LIMIT = os.getenv("RATE_LIMIT", "5/minute")
    
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
