import os
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langgraph.graph import END
# from dotenv import load_dotenv

# load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

@tool
def ask_user_for_clarification(question_for_user: str) -> str:
    """
    Use this tool when the user's request is ambiguous, vague, or missing key information
    that you need to provide a complete and accurate answer. Your goal is to formulate a
    specific, targeted question to ask the user to get the necessary details.
    If the user’s question is already clear, the graph will continue normally.
    """
    # The graph will be interrupted before this function’s body runs.
    print(f"--- Interruption to ask user: {question_for_user} ---")
    return ""

# define the external search tool
tool = TavilySearch(max_results=2)
tools = [tool, ask_user_for_clarification]
