import pytest
import pandas as pd 

from unittest.mock import MagicMock, patch, AsyncMock

from app.clients.yahoo_finance_client import YahooFinanceClient 
from app.clients.alphavantage_client import AlphaVantageClient  

from app.exceptions import InvalidCryptoNameError

class TestYahooFinanceClient:

    def test_fetch_returns_data(self):
        """Test successfull fetch returns a dataframe"""

        mock_df = pd.DataFrame({
            "Open": [100, 102],
            "Close": [98, 89],
            "Volume": [1123, 2212]
        })

        with patch("app.clients.yahoo_finance_client.yf.Ticker") as mock_ticker:
            mock_ticker.return_value.history.return_value = mock_df

            client = YahooFinanceClient()
            result = client.fetch("BTC", "1d", "1h")

            assert not result.empty
            assert "Close" in result.columns

            mock_ticker.assert_called_once_with("BTC-USD")


    def test_fetch_invalid_currency(self):
        """Test invalid crypto name"""

        empty_df = pd.DataFrame()
        with patch("app.clients.yahoo_finance_client.yf.Ticker") as mock_ticker:
            mock_ticker.return_value.history.return_value = empty_df 

            client = YahooFinanceClient()
            with pytest.raises(InvalidCryptoNameError):
                client.fetch("INVALID", "1d", "1m")
         
@pytest.mark.asyncio
class TestAlphaVantageClient:
    async def test_alphavantage_results(self):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"price": "123.55"}

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response


        with patch("app.clients.alphavantage_client.httpx.AsyncClient") as mock_async_client:
            mock_async_client.return_value.__aenter__.return_values = mock_client

            client = AlphaVantageClient()
            result = await client.fetch({"symbol": "BTC"})

            assert result == {"price": "123.55"}


        



