from ddgs import DDGS
import logging
import asyncio

logger = logging.getLogger(__name__)

class SearchService:
    @staticmethod
    async def search_market_data(sector: str):
        """
        Searches for current market data/news for a specific sector in India.
        """
        query = f"{sector} sector India market trends opportunities 2025 2026"
        try:
            # We use standard text search as it is generally more reliable than news for specific queries
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=8))
                
            if not results:
                return "No search results found for the specified sector."
            
            formatted_data = []
            for res in results:
                title = res.get('title', 'No Title')
                body = res.get('body', res.get('snippet', 'No content available'))
                url = res.get('href', 'No URL')
                formatted_data.append(f"Title: {title}\nContent: {body}\nSource: {url}\n---")
            
            return "\n".join(formatted_data)
        except Exception as e:
            logger.error(f"Error during search: {e}")
            # Fallback if specific search fails
            return f"Error gathering data: Search service is currently unavailable or rate-limited. (Internal: {str(e)})"
