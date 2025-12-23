import requests
from typing import Literal, Dict
from app.schemas.env_schema import settings 

from agent.schemas.tool_longterm_prices_schema import LongTermPrices
from app.utils.logger import get_logger

from langchain.tools import tool

logger = get_logger("main")

@tool(args_schema=LongTermPrices)
def fetch_longterm_prices(currency: str,
                          time_stamp: Literal["DAILY", "WEEKLY", "MONTHLY"]) -> Dict: 
                      
    """Fetch daily, weekly or monthly prices prices from external API and store in database
Use this when price data for day, week or month is outdated or you need deeper analysis.

       Args:
        - currency: Name of the cryptocurrency
        - time_stamp: Time period to fetch ("DAILY", "WEEKLY", "MONTHLY")

       Returns:
        - list: A list of prices objects with date, currency, time_period, interval,
                open_price, highes_price, lowest_price, close_price and volume.
        
        """

    logger.info(f"Fetching longterm prices for {currency}: {time_stamp}")

    url = f"{settings.API_BASE_URL}/get_prices"
    params = {
        "currency": currency,
        "time_period": time_stamp,
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
        return f"Could not connect to AlphaVantage. Check network connection."

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        logger.error(f"HTTP {status} for fetching prices for {currency}: {str(e)}")

        if status == 400:
            return f"Currency {currency} not found"
        elif status == 429:
            return f"Rate limit exceeded. Please wait"
        elif status == 502:
            return f"Alpha Vantage API is currently unavailable"

        return f"API Error (HTTP {status}) fetching prices for currency {currency}"

    except Exception as e:
        logger.exception(f"Unexpected error happened while fetching prices for {currency}")
        return f"Unexpected error occurred while fetching prices"

