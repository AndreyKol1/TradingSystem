import psycopg 

from app.database.config import CONN_STRING
from functools import lru_cache

from app.services.get_news import GetNewsCrypto
from app.services.get_prices import GetPricesCrypto
from app.services.get_fear_greed import GetFearGreedIndex
from app.services.get_intraday_prices import IntraDayPricesService

async def get_conn():
    async with await psycopg.AsyncConnection.connect(CONN_STRING) as conn:
        yield conn

@lru_cache 
def get_news_fetcher() -> GetNewsCrypto:
    return GetNewsCrypto()

@lru_cache 
def get_price_fetcher() -> GetPricesCrypto:
    return GetPricesCrypto()

@lru_cache 
def get_fear_greed_fetcher() -> GetFearGreedIndex:
    return GetFearGreedIndex()

@lru_cache 
def get_intraday_price_fetcher() -> IntraDayPricesService:
    return IntraDayPricesService()


