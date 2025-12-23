import pytest 

from pydantic import ValidationError
from agent.schemas.tool_final_output_schema import AgentOutput
from agent.schemas.tool_intraday_prices_schema import FetchIntradayPrices


def test_agent_output(agent_output):

    assert agent_output.score == 1.0

def test_invalid_agent_input_datatype():
    with pytest.raises(ValidationError):
        AgentOutput(
            reasoning="Some reasoning",
            signal="BUY",
            score="not a number",
            confidence="HIGH")

def test_missing_agent_variable():
    with pytest.raises(ValidationError):
             AgentOutput(
                reasoning="Some reasoning",
                signal="BUY",
                score=1.4)

def test_valid_singals():
    for sg in ["BUY", "SELL", "HOLD"]:
        output = AgentOutput(
            reasoning="Some reasoning",
            signal=sg,
            score=1.4,
            confidence="LOW")

        assert output.signal == sg


def test_intraday_prices(valid_intraday_params):
        assert valid_intraday_params.interval == "1m"

def test_invalid_currency_intraday_prices():
    with pytest.raises(ValidationError):
        FetchIntradayPrices(
                currency="BTCC",
                time_stamp="1d",
                interval="2m")

def test_invalid_interval_prices():
    with pytest.raises(ValidationError):
         FetchIntradayPrices(
                currency="BTC",
                time_stamp="1d",
                interval="122m")


@pytest.mark.parametrize("interval", ["1m", "2m", "5m", "15m", "30m", "1h"])
def test_all_valid_intervals(interval):
    output = FetchIntradayPrices(
            currency="BTC", 
            time_stamp="1d", 
            interval=interval)

    assert output.interval == interval

@pytest.mark.parametrize("time_stamp", ["1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y"])
def test_all_valid_timestamps(time_stamp):
    output = FetchIntradayPrices(
            currency="BTC", 
            time_stamp=time_stamp,
            interval="1m")

    assert output.time_stamp == time_stamp 



# write tests for FetchIntradayPrices, etc..

