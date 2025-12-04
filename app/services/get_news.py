from app.utils.logger import get_logger
from app.utils.currency_validation import validate_cryptocurr
from app.schemas.news_schema import CryptoNewsDataSchema
from app.clients.alphavantage_client import AlphaVantageClient
from app.exceptions import  DataParsingError

from datetime import datetime 
from typing import Dict, List


class GetNewsCrypto:
    def __init__(self):
        self.logger = get_logger("main")
        self.client = AlphaVantageClient()

    async def fetch_news(self, currency: str) -> List[CryptoNewsDataSchema]: 
        """Fetch news based on the currecy provided"""
        currency = currency.upper()
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": f"CRYPTO:{currency}",
            }

        validate_cryptocurr(currency) # validate cryptocurrency name

        news_info_json = await self.client.fetch(params)
        news = self._extract_news_data(currency, news_info_json)

        return news
       
    def _extract_news_data(self, currency: str, data: Dict) -> List[CryptoNewsDataSchema]:
        """Extract news from API data""" 

        full_info: List[CryptoNewsDataSchema] = []
        try:
            for doc in data["feed"]:
                currency_ticker = doc["ticker_sentiment"][-1]
                if currency_ticker["ticker"] == f"CRYPTO:{currency}":
                    news_item = CryptoNewsDataSchema(
                        title = doc["title"],
                        summary = doc["summary"],
                        date_published = self._preprocess_date(doc["time_published"]),
                        currency = currency,
                        relevance_score = float(currency_ticker["relevance_score"]),
                        ticker_sentiment_score = float(currency_ticker["ticker_sentiment_score"])
                    )
                    full_info.append(news_item)

        except KeyError as e:
            self.logger.error(f"Missing expected field in API response: {str(e)}")
            raise DataParsingError(f"Missing field: {str(e)}")

        except Exception as e:
            self.logger.exception(f"Unexpected error while parsing data: {str(e)}")
            raise

        self.logger.info(f"""Successfully extracted title, summary, date, relevance score
                             and ticker sentiment score from the returned data for the {currency}""")

        return full_info

    @staticmethod 
    def _preprocess_date(date: str) -> str:
        format_data = "%Y%m%dT%H%M%S"
        dt = datetime.strptime(date, format_data)
        return dt.strftime("%Y-%m-%d")
    
