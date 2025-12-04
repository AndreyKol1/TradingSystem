from app.utils.logger import get_logger 
from app.schemas.prices_schema import CryptoPricesDataSchema
from app.utils.currency_validation import validate_cryptocurr
from app.clients.alphavantage_client import AlphaVantageClient
from app.exceptions import DataParsingError

from typing import List, Dict


class GetPricesCrypto:
    def __init__(self):
        self.logger = get_logger("main")
        self.client = AlphaVantageClient()

    async def fetch_prices(self, currency: str = "BTC", time_period: str = "DAILY") -> List[CryptoPricesDataSchema]:
        """Fetch prices based on provided crypto currency and time period:
           Possible periods: DAILY, WEEKLY, MONTHLY"""

        currency = currency.upper()

        self._validate_time_period(time_period) # validate time period
        validate_cryptocurr(currency) # validate cryptocurrency name
        params = {
            "function": f"DIGITAL_CURRENCY_{time_period}",
            "symbol": currency,
            "market": "USD"
        }

        prices_info_json = await self.client.fetch(params)
        prices = self._extract_price_data(currency, time_period, prices_info_json)
        return prices
        
    def _extract_price_data(self, currency: str, time_period: str, data: Dict) -> List[CryptoPricesDataSchema]:
        """Extract data from the returned json object"""

        full_prices_info: List[CryptoPricesDataSchema] = []

        try:
            for date, prices in data[f"Time Series (Digital Currency {time_period.lower().capitalize()})"].items():
                currency_item = CryptoPricesDataSchema(
                        date_price = date,
                        currency = currency,
                        time_period = time_period.upper(),
                        open_price = prices["1. open"],
                        high = prices["2. high"],
                        low = prices["3. low"],
                        close = prices["4. close"],
                        volume = prices["5. volume"]
                )
                full_prices_info.append(currency_item)

        except KeyError as e:
            self.logger.error(f"Missing expected field in API response: {str(e)}")
            raise DataParsingError(f"Missing field: {str(e)}")

        except Exception as e:
            self.logger.exception(f"Unexpected error while parsing data: {str(e)}")
            raise

        self.logger.info(f"""Successfully extracted date, open price, highest price, 
                                lowest price, close price and volume for the {currency}""")

        return full_prices_info

    @staticmethod
    def _validate_time_period(time_period: str) -> None:
        available_periods = ["DAILY", "WEEKLY", "MONTHLY"]
        if time_period.upper() not in available_periods:
            raise ValueError(f"Invalid period: {time_period}")
