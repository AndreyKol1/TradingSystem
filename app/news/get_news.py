import os
import httpx

from dotenv import load_dotenv
from typing import List
from app.utils.logger import get_logger
from app.schemas.news_schema import CryptoNewsDataSchema

load_dotenv()

class GetNewsCrypto:
    def __init__(self):
        self.crypto_key = os.getenv("CRYPTO_NEWS_API")
        self.logger = get_logger("main")

    async def fetch_news(self, currency: str) -> List[CryptoNewsDataSchema]: 
        """Fetch news based on the currecy provided"""
        try:
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=CRYPTO:{currency}&apikey={self.crypto_key}'
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            response.raise_for_status()
            data = response.json()

            self.logger.info("Successfully extracted news from the wes-site")

            full_info: List[CryptoNewsDataSchema] = []

            for doc in data["feed"]:
                currency_ticker = doc["ticker_sentiment"][-1]
                if currency_ticker["ticker"] == f"CRYPTO:{currency}":
                    news_item = CryptoNewsDataSchema(
                        title = doc["title"],
                        summary = doc["summary"],
                        date_published = self.preprocess_date(doc["time_published"]),
                        ticker = currency_ticker["ticker"],
                        relevance_score = float(currency_ticker["relevance_score"]),
                        ticker_sentiment_score = float(currency_ticker["ticker_sentiment_score"])
                    )
                    full_info.append(news_item)
                                                              
            self.logger.info("Successfully extracted relevant info from the returned data")
            return full_info

        except Exception as e:
            self.logger.error(f"The error occured, possibly you wrote invalid crypto currency name of exceeded API usage: {str(e)}")
            raise

    @staticmethod 
    def preprocess_date(date: str) -> str:
        sliced_date = date[:8] # slice to YYMMDD
        year = sliced_date[:4]
        month = sliced_date[4:6]
        day = sliced_date[6:]

        proper_date = f"{year}-{month}-{day}"
        return proper_date
