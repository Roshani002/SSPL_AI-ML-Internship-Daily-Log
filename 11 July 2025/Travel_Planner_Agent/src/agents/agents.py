import os
from crewai import Agent, LLM
from src.tools.custom_tool import search_internet
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Destination Researcher agent
destination_researcher = Agent(
    role="Destination Researcher",
    goal="Find up-to-date information about destinations, seasons, and travel conditions.",
    backstory="You are a travel expert who specializes in gathering accurate and current information about travel destinations.",
    llm=llm,
    verbose=True,
    tools=[search_internet]
)

#  Attractions Specialist agent
attractions_specialist = Agent(
    role="Attractions Specialist",
    goal="Discover the best attractions, activities, and hidden gems at the destination.",
    backstory="You are an expert who knows how to find the most interesting attractions and activities that match travelers' preferences.",
    llm=llm,
    verbose=True,
    tools=[search_internet]
)

# Local Guide agent
local_guide = Agent(
    role="Local Guide",
    goal="Provide insider tips, cultural insights, and practical travel advice.",
    backstory="You are a knowledgeable local guide who knows all the insider tips, cultural nuances, and practical information that travelers need.",
    llm=llm,
    verbose=True,
    tools=[search_internet]
)
