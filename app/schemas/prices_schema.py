from pydantic import BaseModel
from datetime import date, datetime

from typing import Optional, List, Union

class CryptoPricesDataSchema(BaseModel):
    date_price : Union[date, datetime]
    currency: str
    time_period: str
    interval: Optional[str] = None 
    open_price: float
    high: float
    low: float
    close: float
    volume: float
