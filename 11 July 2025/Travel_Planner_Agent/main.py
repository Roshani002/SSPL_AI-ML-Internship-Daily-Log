# backend
import os
from src.agents.agents import destination_researcher, attractions_specialist, itinerary_planner, local_guide
from src.tasks.tasks import create_destination_tasks
from crewai import Crew, Process
from dotenv import load_dotenv

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["MODEL"] = os.getenv("MODEL")

# Get user input
destination = input("Enter your travel destination: ")
travel_dates = input("Enter your travel dates: ") 
duration_days = int(input("How many days is your trip? "))
preferences = input("Enter your travel preferences (Cultural & Museums, Food & Culinary): ") 
budget = input("Enter your budget level (budget, moderate, luxury) ") 

print(f"\nGenerating travel plan for {destination}...")

# tasks for the destination
tasks = create_destination_tasks(
    destination=destination, 
    travel_dates=travel_dates,
    duration_days=duration_days,
    preferences=preferences,
    budget=budget
)

# crew with the agents and customized tasks
crew = Crew(
    agents=[destination_researcher, attractions_specialist, itinerary_planner, local_guide],
    tasks=tasks,
    verbose=1,
    process=Process.sequential  
)

# Kick off the execution process
results = crew.kickoff()

print(results)

