from fastapi import APIRouter

from agent.utils.tracing import langfuse_handler
from agent.agent import initialize_agent 
from agent.schemas.tool_final_output_schema import AgentOutput

from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/analyze")
def analyze_crypto(query: str) -> AgentOutput:
    agent = initialize_agent()

    result = agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"callbacks": [langfuse_handler],
                "recursion_limit": 25}
    )
    return result["structured_response"]
