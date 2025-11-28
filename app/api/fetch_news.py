from fastapi import APIRouter, Depends
from app.dependencies import get_conn

from app.dependencies import get_news_fetcher


router = APIRouter()

@router.post("/get_news")
async def add_news(currency: str, conn=Depends(get_conn)):
    news_class_cached = get_news_fetcher()
    news = await news_class_cached.fetch_news(currency)
    async with conn.cursor() as cursor:
        for doc in news:
            await cursor.execute("""INSERT INTO crypto_news
                                    (title, summary, publish_time, ticker, relevance_score, ticker_sentiment)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (ticker, title, publish_time) DO NOTHING""",
                                    
                                    (doc.title, doc.summary, doc.date_published,
                                     doc.ticker, doc.relevance_score, doc.ticker_sentiment_score))

        await conn.commit()


    return {"message": f"Values successfully logged"}
