from langgraph.graph import StateGraph, END
from state import State, memory 
from nodes import flight_node, itinerary_node
from agents.chatbot_agent.chatbot import chatbot_node

builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)
builder.add_node("itinerary_agent", itinerary_node)
builder.add_node("flight_agent", flight_node)

builder.set_entry_point("chatbot")

builder.add_conditional_edges(
    "chatbot",
    lambda state: state["next"], 
    {
        "flight_agent": "flight_agent",
        "itinerary_agent": "itinerary_agent",
        "human_interrupt": END,  # The graph waits for the next user input
        "__end__": END # The conversation is finished
    }
)

builder.add_edge("flight_agent",END)
builder.add_edge("itinerary_agent", END)

graph = builder.compile(checkpointer=memory)