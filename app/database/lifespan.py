import psycopg

from contextlib import  asynccontextmanager
from app.database.config import CONN_STRING 
from app.utils.logger import get_logger
from app.database.tables import create_crypto_news_table, create_crypto_prices_table, create_fear_greed_table

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app):
    logger.info("Startup: Checking database tables...")
    try:
        async with await psycopg.AsyncConnection.connect(CONN_STRING) as conn: # creating a databse instance
            async with conn.cursor() as cur: # creating a cursor with which we can query the db
                await cur.execute(create_crypto_news_table())
                await cur.execute(create_crypto_prices_table())
                await cur.execute(create_fear_greed_table())
                    
                await conn.commit() # Make the changes to the database persistent
                logger.info("Startup: Tables 'crypto_news, crypto_prices, fear_greed_index' are ready.")

    except Exception as e:
        logger.error(f"Startup Error: Could not connect to DB. {e}")
        raise 

    yield 

    logger.info("Shutdown: App is closing.")

