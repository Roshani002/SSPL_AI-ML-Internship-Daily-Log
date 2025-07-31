from langchain_community.tools.tavily_search import TavilySearchResults
from crewai.tools import tool

@tool
def search_internet(query: str) -> str:
    """Search the internet for the given query, restricted to the last `recent_days` days, and return the top 5 results."""
    search = TavilySearchResults(
        max_results=1,
    )
    results = search.invoke(query)
    return "\n".join([result['content'] for result in results])
