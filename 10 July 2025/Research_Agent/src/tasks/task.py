from crewai import Task
from src.agents.agent import researcher

def create_task(topic):
    research_task = Task(
        description=(
            f"Conduct a comprehensive analysis of the latest advancements in {topic} in 2025. "
            "Identify key trends, breakthrough technologies, and potential industry impacts. "
            "Compile your findings in a detailed report in only 100 words. "
            "Make sure to check with a human if the draft is good before finalizing your answer."
        ),
        expected_output=f'A comprehensive full report in 100 words on the latest details for {topic} in 2025, leave nothing out',
        agent=researcher,
        human_input=True
    )
    return research_task