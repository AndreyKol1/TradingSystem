# Shared fixtures go here
# Start empty - add fixtures as you need them

import pytest 
from agent.schemas.tool_final_output_schema import AgentOutput
from agent.schemas.tool_intraday_prices_schema import FetchIntradayPrices



@pytest.fixture
def agent_output():
    return AgentOutput(
        reasoning="Some reasoning",
        signal="BUY",
        score=1.0,
        confidence="HIGH")

@pytest.fixture
def valid_intraday_params():
    return FetchIntradayPrices(
            currency="BTC",
            time_stamp="1d",
            interval="1m")
