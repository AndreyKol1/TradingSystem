from app.schemas.news_schema import CryptoNewsData

from typing import List, Dict

def validate_crypto_news(raw_news: List[Dict]) -> List[CryptoNewsData]:
    validated = []
    for item in raw_news:
        validated.append(CryptoNewsData.model_validate(item))
    return validated

