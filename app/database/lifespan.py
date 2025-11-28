from contextlib import  asynccontextmanager
from app.database.config import CONN_STRING 
from app.utils.logger import get_logger
import psycopg

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app):
    logger.info("Startup: Checking database tables...")
    try:
        async with await psycopg.AsyncConnection.connect(CONN_STRING) as conn: # creating a databse instance
            async with conn.cursor() as cur: # creating a cursor with which we can query the db
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS crypto_news(
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        publish_time DATE NOT NULL,
                        ticker VARCHAR(20) NOT NULL,
                        relevance_score  REAL NOT NULL,
                        ticker_sentiment REAL NOT NULL,

                        CONSTRAINT unique_news_item UNIQUE (ticker, title, publish_time)
                        )
                    """)
                await conn.commit() # Make the changes to the database persistent
                logger.info("Startup: Table 'news_db' is ready.")

    except Exception as e:
        logger.error(f"Startup Error: Could not connect to DB. {e}")
        raise 

    yield 

    logger.info("Shutdown: App is closing.")

