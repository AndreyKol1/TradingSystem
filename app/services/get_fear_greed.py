from app.utils.logger import get_logger
from app.schemas.fear_greed_idx_schema import FearGreedIndexSchema
from app.clients.alternativeme_client import AlternativeMeClient
from app.exceptions import DataParsingError

from datetime import datetime
from typing import Dict 

class GetFearGreedIndex:
    def __init__(self):
        self.logger = get_logger("main")
        self.client = AlternativeMeClient()

    async def fetch_fear_greed_index(self) -> FearGreedIndexSchema:
        """Fetch fear and greed index"""

        extracted_data = await self.client.fetch()
        processed_values = self._extract_fear_greed_data(extracted_data)

        return processed_values
        
    def _extract_fear_greed_data(self, data: Dict) -> FearGreedIndexSchema:
        """Extract fear greed index"""

        try:
            index_info = FearGreedIndexSchema(
                classification = data["data"][0]["value_classification"],
                value = data["data"][0]["value"],
                time_stamp = self._convert_unix_timestamp(data["data"][0]["timestamp"])
            )
        
        except KeyError as e:
            self.logger.error(f"Missing expected field in API response: {str(e)}")
            raise DataParsingError(f"Missing field: {str(e)}")

        except Exception as e:
            self.logger.exception(f"Unexpected error during values extraction: {str(e)}")
            raise

        return index_info 

    @staticmethod
    def _convert_unix_timestamp(time_stamp: str) -> str:
        """Convert unix time to current time"""

        ts = int(time_stamp)
        value = datetime.fromtimestamp(ts)
        return value.strftime("%Y-%m-%d") 
