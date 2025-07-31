from crewai.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

# Define a Tavily search tool
@tool
def search_internet(query: str, recent_days: int=7) -> str:
    """Search the internet for the given query, restricted to the last `recent_days` days, and return the top 5 results."""
    search = TavilySearchResults(
        max_results=5,
        recent_days = recent_days  # Limit the number of results
    )
    try:
        results = search.invoke(query)
        formatted = ""
        for r in results:
            pub = r.get("published_date", "unknown date")
            formatted += f"📅 *Published:* {pub}\n"
            formatted += f"🔗 Source: {r.get('url','–')}\n"
            formatted += f"**{r.get('title','–')}**\n"
            formatted += r.get("content","No content") + "\n\n"
        return formatted or "No recent results found."
    except Exception as e:
        return f"Error searching the internet: {str(e)}"
