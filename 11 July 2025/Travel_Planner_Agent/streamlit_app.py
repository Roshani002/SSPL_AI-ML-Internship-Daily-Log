# edited prompts, without human in loop
import re
import os
from dotenv import load_dotenv
from dateutil import parser
from datetime import date
import streamlit as st
from src.agents.agents import destination_researcher, attractions_specialist, local_guide
from src.tasks.tasks import create_destination_tasks
from crewai import Crew, Process

# Load environment variables
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")

# Streamlit setup
st.set_page_config(page_title="Travel Planner Agent", layout="wide")
st.title("Travel Planner Agent")

# Taking user input
with st.form("travel_form"):
    dest       = st.text_input("Destination", placeholder="e.g., Mount Abu")
    travel_dt  = st.date_input("Travel Date")
    duration   = st.number_input("Duration (days)", min_value=1)
    preference_options = [
    "Cultural & Museums",
    "Food & Culinary",
    "Nature & Hiking",
    "Adventure & Sports",
    "Beaches & Relaxation",
    "Wildlife & Safaris",
    "Historical Sites",
    "Nightlife",
    "Shopping",
    "Wellness & Spa",
    "Family & Kids"
    ]  
    selected_prefs = st.multiselect(
        "Select your travel preferences",
        options=preference_options,
    )
    preferences = ", ".join(selected_prefs)

    # budget
    budget = st.selectbox("Budget Level", ["low", "moderate", "luxury"])
    submit = st.form_submit_button("Generate Travel Plan")

if submit:
    if not dest:
        st.error("Please enter a destination.")
    else:
        with st.spinner("🛠️  Generating your travel plan..."):
            # run crew
            tasks = create_destination_tasks(destination=dest,travel_start=travel_dt,duration_days=duration,preferences=preferences,budget=budget)
            crew = Crew(
                agents=[destination_researcher, attractions_specialist, local_guide],
                tasks=tasks,
                verbose=True,
                process=Process.sequential,
            )
            results = crew.kickoff()
            for task_output in results.tasks_output:
                st.markdown(task_output.raw)


            