from state import State
from agents.flight_agent.flight_agent import flight_agent
from langchain_core.messages import AIMessage, HumanMessage
from agents.itinerary_agent.itinerary_agent import itinerary_agent


def itinerary_node(state: State) -> dict:
    """Invokes the itinerary agent and returns its direct, human-readable output."""

    # conversation_summary = "\n".join([msg.content for msg in state["messages"] if hasattr(msg, 'content')])
    # response = itinerary_agent.invoke({"user_request": conversation_summary})
    user_request = state["messages"][-1].content
    response = itinerary_agent.invoke({"user_request": user_request})
    return {"messages": [AIMessage(content=response.content)]}

def flight_node(state: State) -> dict:
    """Invokes the flight agent and returns its direct, human-readable output."""

    result = flight_agent.invoke({"messages": state["messages"]})
    final_answer = result["messages"][-1].content
    
    return {"messages": [AIMessage(content=final_answer)]}


