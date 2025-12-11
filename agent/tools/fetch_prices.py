import requests
from typing import Literal
from app.schemas.env_schema import settings 

from langchain.tools import tool

def fetch_intraday_prices(currency: str,
                      time_stamp: Literal["1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y"],
                      interval: Literal["1m", "2m", "5m", "15m", "30m", "1h"]) -> None:

    """Fetch fresh intraday prices from external API and store in database

       Use this when price data is missing or stale

       Args:
        - currency: Name of the cryptocurrency
        - time_stanp: Time period to fetch ("1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y"),
        - interval: Price interval ("1m", "2m", "5m", "15m", "30m", "1h")

        """

    url = f"{settings.API_BASE_URL}/get_intraday_prices"
    params = {
        "currency": currency,
        "time_stamp": time_stamp,
        "interval": interval
    }
    response = requests.post(url, params=params)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    lws = fetch_intraday_prices("BTC", "1d", "30m")
    print(lws)

