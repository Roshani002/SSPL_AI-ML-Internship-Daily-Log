import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uuid
# from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage

from utils.tools import tools
from utils.state import State
from utils.nodes import tool_node
from langgraph.checkpoint.memory import MemorySaver


memory = MemorySaver()

# --- Setup ---
# load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# System Prompt and LLM 
system_prompt = (
    "You are a helpful and diligent AI assistant. Your primary goal is to provide accurate and relevant answers. "
    "Critically evaluate the user's request. If the request is vague, ambiguous, or missing crucial details, "
    "do not try to guess. Instead, use the 'ask_user_for_clarification' tool to ask a specific question "
    "that will help you understand the user's needs better. Only after you have enough information "
    "should you provide a final answer."
)

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)

# Define Graph Nodes 
def chatbot(state: State):
    print("---Processing---")
    messages_with_system_prompt = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm_with_tools.invoke(messages_with_system_prompt)
    return {"messages": [response]}

# Define Conditional Logic
def route_after_chatbot(state: State) -> str:
    """Decide where to go after the chatbot has run."""
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return END
    # Check if the AI wants to ask the user for clarification
    if any(tc["name"] == "ask_user_for_clarification" for tc in last_message.tool_calls):
        return "ask_user_for_clarification"
    # Otherwise, route to standard tools
    return "tools"

# Build the Graph 
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("ask_user_for_clarification", interrupt)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", route_after_chatbot)
graph_builder.add_edge("tools", "chatbot")

# Compile the graph
graph = graph_builder.compile(checkpointer=memory)

# # Interactive Loop 
# thread_id = str(uuid.uuid4())
# config = {"configurable": {"thread_id": thread_id}}

# print("AI Assistant initialized. How can I help you? (Type 'exit' to end)")

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         break

#     events = graph.stream({"messages": [("user", user_input)]}, config, stream_mode="values")
#     for event in events:
#         if "messages" in event:
#             event["messages"][-1].pretty_print()

#     snapshot = graph.get_state(config)
#     if snapshot.next and snapshot.next[0] == "ask_user_for_clarification":
#         print("\n--- CLARIFICATION NEEDED ---")
#         ai_message = snapshot.values["messages"][-1]

#         # Find the clarification tool call
#         clarification_call = next(
#             (tc for tc in ai_message.tool_calls if tc["name"] == "ask_user_for_clarification"),
#             None
#         )
#         if clarification_call:
#             # Get the question the AI formulated for the user
#             ai_question = clarification_call["args"]["question_for_user"]
#             print(f">>> '{ai_question}'")
#             user_response = input("Your Answer: ")
#             # Create a ToolMessage to feed the user's answer back into the graph
#             tool_message = ToolMessage(content=user_response, tool_call_id=clarification_call["id"])
#             # Resume the graph with the new information
#             events = graph.stream({"messages": [tool_message]}, config, stream_mode="values")
#             for event in events:
#                 if "messages" in event:
#                     event["messages"][-1].pretty_print()
