import requests
from typing import Dict 
from agent.schemas.tool_news_schema import FetchNewsAPI 
from app.schemas.env_schema import settings 
from app.utils.logger import get_logger

from langchain.tools import tool

logger = get_logger("main")

@tool(args_schema=FetchNewsAPI)
def fetch_news(currency: str) -> Dict:
    """Fetch fresh news on the given cryptocurrency from external API and store in database

       Use this when there is lack of data or no recent news are in database. 

       Args:
        - currency: Name of the cryptocurrency

       Returns: 
        list: A list of news objects with title, summary, date_published, currency,
              relevance score and ticker sentiment score.

        """

    url = f"{settings.API_BASE_URL}/get_news"
    params = {
        "currency": currency,
    }

    try:
        response = requests.post(url, params=params, timeout=20)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching prices for {currency}")
        return f"Request timed out. The API may be slow or unavailable"

    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for fetching prices for {currency}")
        return f"Could not connect to API endpoint. Check network connection."

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        logger.error (f"HTTP {status} for fetching prices for {currency}: {str(e)}")

        if status == 400:
            return f"Currency {currency} not found"
        elif status == 429:
            return f"Rate limit exceeded. Please wait 24 hours to get more requests."
        elif status == 502:
            return f"Alpha Vantage API is currently unavailable"

        return f"API Error (HTTP {status}) fetching news for currency {currency}"

    except Exception as e:
        logger.exception(f"Unexpected error happened while fetching prices for {currency}")
        return f"Unexpected error occurred while fetching prices"

