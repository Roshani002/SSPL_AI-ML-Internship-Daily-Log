from crewai import Task
from datetime import date
from src.agents.agents import destination_researcher, attractions_specialist, local_guide

def create_destination_tasks(destination, travel_start, duration_days, preferences, budget):
    """
    Create tasks customized for a specific travel destination.
    """
    today = date.today().isoformat()
    travel_str = travel_start.strftime("%B %d, %Y")
    # if trip is future, ask for forecast; else current weather
    if travel_start > date.today():
        weather_line = f"Forecast the weather in {destination} on {travel_str}."
    else:
       weather_line = f"Report current weather and best season to visit (as of {today})."

    # research task for the Destination Researcher agent
    destination_research_task = Task(
        description=f"""Research comprehensive information about {destination} as a travel destination and {weather_line}:
        1. Current weather and best seasons to visit
        2. Local customs, etiquette, and cultural considerations
        3. Safety information and any travel advisories
        4. Transportation options within the city/area
        5. Language considerations and useful phrases
        6. Currency and payment information and General cost of living for travelers with a {budget} budget
        8. Any current events or festivals happening around {travel_start}
        (Always cite the publication date of each source.)
       
        Be factual, thorough, and objective. Include only verified information from your search results.
        Format your response in clear sections with headings.
        Please output **Markdown**: use `## Section Title` for each section and simple `- bullet points` for lists.""",
        agent=destination_researcher,
        expected_output=f"A comprehensive report about {destination} with factual information organized in sections",
    )
    
    # task for the Attractions Specialist agent
    attractions_task = Task(
        description=f"""Identify the best attractions and activities in {destination} that match these preferences: {preferences}.
        For a {budget} budget traveler spending {duration_days} days there.
        
        Include for each attraction:
        1. Name and brief description
        2. Why it's worth visiting
        3. Recommended time to spend there
        4. Entrance fees or costs if available
        5. Best time of day/week to visit
        6. Insider tips to enhance the experience
        
        Group attractions by type (museums, outdoor activities, dining, etc.)
        Include some hidden gems or local favorites, not just tourist hotspots.

        Please output **Markdown**: use `## Section Title` for each section and simple `- bullet points` for lists.""",
        agent=attractions_specialist,
        expected_output=f"A detailed list of attractions and activities in {destination} organized by type",
    )
    
    # task for the Local Guide agent
    guide_task = Task(
        description=f"""Create a comprehensive travel guide for {destination} to complement the itinerary.
        
        Now, build the practical travel guide for **{destination}**:
        1. Give Each Attraction name and short description, Why it's worth visiting, Recommended time to spend there, Entrance fees or costs (if available), Best time of day/week to visit and if any tips to enhance experience
        2. Health and safety advice specific to this destination
        3. Dining: 10 restaurants or street-food spots & local thalis with rates within {budget}
        4. Accommodation: 10 Hotels for staying ranked lowest to highest rate per night within {budget} budget
        5. Transportation: available modes & your recommendation by {budget} & time constraints 
        6. Languages: native language + common tourist languages + key phrases of 
        7. Local food specialties worth trying and famous food dishes of {destination}
        8. Shopping recommendations for authentic souvenirs and markets you must visit
        9. Cultural insights: Cultural insights for {destination} — including etiquette, taboos, dress codes, key phrases, social norms, and festivals.”
        10. Any event or festival during {travel_start} to {duration_days}-days trip 

        Make this guide practical, specific to {destination}, and aligned with the preferences: {preferences}.
        Format with clear headings and concise bullet points where appropriate.
        Before finalizing, request human input to confirm: dietary preference (veg, non-veg, or mix), number of travelers, preferred sleep time, lowest and highest budget for hotels and food, and preferred transportation mode with budget.
        after getting human input give your final output.
        Please output **Markdown**: use `## Section Title` for each section and simple `- bullet points` for lists.""",
        agent=local_guide,
        expected_output=f"A practical travel guide for {destination} with tips and cultural insights",
        human_input=True
    )
    
    return [destination_research_task, attractions_task, guide_task]

