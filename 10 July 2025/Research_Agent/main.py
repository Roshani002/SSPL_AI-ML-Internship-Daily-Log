import os
import sys
import streamlit as st
from crewai import Crew
from src.agents.agent import researcher, StreamToExpander
from src.tasks.task import create_task
from dotenv import load_dotenv

load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")

st.set_page_config(page_title="Research Agent", layout="wide")
st.title("Research Agent")

topic = st.text_input("Topic Name", placeholder="Enter topic to research")
submit = st.button(label="Submit")

if submit:
    if not topic:
        st.error("Please enter a topic")
    else:
        # logs_expander = st.expander("🤖 **Agents at work...**", expanded=True)
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=2000, border=False):
                sys.stdout = StreamToExpander(st)
                task = create_task(topic)
                crew = Crew(
                    agents=[researcher],
                    tasks=[task],
                    verbose=True
                )
                result = crew.kickoff()
            status.update(label="Research is ready!", state="complete", expanded=False)

        st.subheader(f"Here is your detailed research about {topic}", anchor=False, divider="rainbow")
        for task_output in result.tasks_output:
            st.markdown(task_output.raw)
        

        