import os
import re
import streamlit as st
from crewai import Agent, LLM
from dotenv import load_dotenv
from src.tools.tool import search_internet

load_dotenv(override=True)

llm = LLM(
    model="openrouter/deepseek/deepseek-r1-0528:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
    st.markdown("---")
    # debugging
    print("Type of step_output:", type(step_output))
    print("Contents of step_output:", step_output)
    # Handle ToolResult object
    if hasattr(step_output, "result"):
        result = step_output.result

        st.markdown("### 🔍 Tool Result Output")

        if isinstance(result, str):
            # Split lines 
            lines = result.strip().split("\n")
            for line in lines:
                if line.startswith("Title: "):
                    st.markdown(f"**Title:** {line[7:]}")
                elif line.startswith("Link: "):
                    st.markdown(f"**Link:** {line[6:]}")
                elif line.startswith("Snippet: "):
                    st.markdown(f"**Snippet:** {line[9:]}")
                elif line.startswith("## "):
                    st.markdown(f"### {line[3:]}")
                elif line.startswith("# "):
                    st.markdown(f"## {line[2:]}")
                elif line.startswith("### "):
                    st.markdown(f"**{line}**")
                else:
                    st.markdown(line)
        else:
            st.markdown(str(result))
    else:
        st.markdown("⚠️ No `result` found in ToolResult.")
        st.markdown(str(step_output))

researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in given topic',
    backstory=(
        "You are a Senior Research Analyst at a leading tech think tank. "
        "Your expertise lies in identifying emerging trends and detailed infomation for given topic."
        "You have a knack for dissecting complex data and presenting actionable insights."
    ),
    verbose=True,
    llm=llm,
    allow_delegation=False,
    tools=[search_internet],
    step_callback=streamlit_callback,
)

# Print agent process to Streamlit app container  
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  
        self.color_index = 0  

    def write(self, data):
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)
            cleaned_data = cleaned_data.replace(
                "Entering new CrewAgentExecutor chain",
                f":{self.colors[self.color_index]}[🔬 New Research Chain]")  
            
        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

       