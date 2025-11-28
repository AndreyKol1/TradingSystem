import psycopg 

from app.database.config import CONN_STRING
from functools import lru_cache

from app.news.get_news import GetNewsCrypto

async def get_conn():
    async with await psycopg.AsyncConnection.connect(CONN_STRING) as conn:
        yield conn

@lru_cache 
def get_news_fetcher() -> GetNewsCrypto:
    return GetNewsCrypto()

