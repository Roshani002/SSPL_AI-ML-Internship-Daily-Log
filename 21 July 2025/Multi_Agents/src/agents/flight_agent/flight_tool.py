import os
import requests
from langchain_core.tools import tool
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


def format_flight_duration(minutes: int) -> str:
    """Converts duration in minutes to a 'HHh MMm' format."""
    if not isinstance(minutes, int):
        return "N/A"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"

def get_cabin_class_name(class_id: int) -> str:
    """Converts cabin class ID to its name."""
    class_map = {1: "Economy", 2: "Premium Economy", 3: "Business", 4: "First"}
    return class_map.get(class_id, "Unknown")

def format_single_flight(flight: Dict, currency: str) -> str:
    """
    Takes a single flight object from the API response and formats it into a detailed,
    human-readable string as specified.
    """
    
    # --- Overall Flight Summary ---
    price = flight.get('price', 'N/A')
    airline_names = ", ".join(flight.get("airlineNames", ["N/A"]))
    stops = flight.get("stops", 0)
    stops_text = "Non-Stop" if stops == 0 else f"{stops} Stop(s)"
    total_duration = format_flight_duration(flight.get('duration'))
    
    summary = (
        f"✈️ **{airline_names}**\n"
        f"  - **Total Price:** {price} {currency}\n"
        f"  - **Total Duration:** {total_duration}\n"
        f"  - **Stops:** {stops_text}\n"
    )

    # --- Detailed Segments / Legs ---
    segments = flight.get("segments", [])
    segment_details = []
    
    for i, segment in enumerate(segments):
        airline = segment.get("airline", {})
        leg_str = (
            f"\n  **Leg {i+1}: {segment.get('departureAirportCode')} to {segment.get('arrivalAirportCode')}**\n"
            f"    - Airline: {airline.get('airlineName', 'N/A')} (Flight {airline.get('flightNumber', 'N/A')})\n"
            f"    - Aircraft: {segment.get('aircraftName', 'N/A')}\n"
            f"    - Cabin Class: {get_cabin_class_name(segment.get('cabinClass'))}\n"
            f"    - Departs: {segment.get('departureTime')} on {segment.get('departureDate')} from {segment.get('departureAirportName')} ({segment.get('departureAirportCode')})\n"
            f"    - Arrives: {segment.get('arrivalTime')} on {segment.get('arrivalDate')} at {segment.get('arrivalAirportName')} ({segment.get('arrivalAirportCode')})\n"
            f"    - Leg Duration: {format_flight_duration(segment.get('durationMinutes'))}"
        )
        segment_details.append(leg_str)

    return summary + "".join(segment_details)

@tool
def flight_tool(
    departureId: str,
    arrivalId: str,
    departureDate: str,
    adults: int = 1,
    cabinClass: Optional[int] = 1,
    currency: str = "USD"
):
    """
    Searches for one-way flights using the Flights Scraper Sky API and returns detailed information for each found flight.
    - departureId: IATA code for departure (e.g., 'JFK').
    - arrivalId: IATA code for arrival (e.g., 'LOS').
    - departureDate: Date in 'YYYY-MM-DD' format.
    - adults: Number of adult passengers.
    - cabinClass: 1 for Economy, 2 for Premium Economy, 3 for Business, 4 for First.
    - give price in indian rupees
    """
    if not RAPIDAPI_KEY:
        return "RapidAPI key is not configured. Please check your .env file."

    api_url = "https://flights-sky.p.rapidapi.com/google/flights/search-one-way"
    api_host = "flights-sky.p.rapidapi.com"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": api_host
    }

    params = {
        "departureId": departureId,
        "arrivalId": arrivalId,
        "departureDate": departureDate,
        "adults": str(adults),
        "cabinClass": str(cabinClass),
        "currency": currency
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})

        # Process each flight using the detailed formatter function
        top_flights = data.get("topFlights", [])
        other_flights = data.get("otherFlights", [])

        all_flights = top_flights + other_flights

        if not all_flights:
            return f"No flights found for the route {departureId} to {arrivalId} on {departureDate}."
        
        formatted_flights = [format_single_flight(flight, currency) for flight in all_flights]
        
        # Join all the formatted flight details with a clear separator
        separator = "\n\n" + ("-" * 50) + "\n\n"
        return separator.join(formatted_flights)

    except requests.exceptions.HTTPError as err:
        error_details = err.response.json()
        error_message = error_details.get("message", "An unknown API error occurred.")
        print(f"!!! RAPIDAPI HTTP ERROR !!!\n{error_message}")
        # Pass the specific error back to the agent.
        return f"Error: The flight search failed. The API returned the following error: '{error_message}'"
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: An unexpected programming error occurred: {str(e)}"