from google import genai
from config import Config
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        if Config.GEMINI_API_KEY:
            self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        else:
            self.client = None

    async def analyze_sector(self, sector: str, market_data: str):
        """
        Uses Gemini API to analyze collected information and generate a report.
        """
        if not self.client:
            return "AI Analysis Error: GEMINI_API_KEY not configured."

        prompt = f"""
        You are a senior market analyst specializing in the Indian economy.
        Analyze the following market data collected for the '{sector}' sector in India:
        
        {market_data}
        
        Generate a highly professional and structured Market Analysis Report in Markdown format.
        The report should include:
        1. **Executive Summary**: Overview of the current state of the {sector} sector in India.
        2. **Current Trade Opportunities**: Specific niches or areas where trade is booming or has potential.
        3. **Key Market Drivers**: Factors driving growth or change.
        4. **Risks and Challenges**: Obstacles that traders or investors might face.
        5. **Future Outlook (2025-2026)**: Predictions based on current trends.
        6. **Conclusion**: Final recommendation.

        Use bold headings, tables if applicable, and bullet points for readability.
        Ensure the tone is professional, analytical, and data-driven.
        """

        try:
            # Using the new google-genai SDK syntax
            response = self.client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini analysis: {e}")
            return f"Error analyzing data with AI: {str(e)}"
