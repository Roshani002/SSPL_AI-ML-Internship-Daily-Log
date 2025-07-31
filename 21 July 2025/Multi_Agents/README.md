# ✈️ TravelBot: Multi-Agent Travel Planner with LangGraph

TravelBot is a multi-agent travel planning assistant built using [LangGraph](https://docs.langgraph.dev/), [LangChain](https://www.langchain.com/), and [Streamlit](https://streamlit.io/). It routes user queries to either a **Flight Search Agent** or an **Itinerary Planning Agent** based on context.

---

## 🧠 Features

- 🧭 Intelligent **Chatbot Agent** (Router)
- 🧳 **Itinerary Planner Agent** with day-wise budgeted plan
- 🛫 **Flight Finder Agent** with RapidAPI integration
- 💬 CLI + Streamlit UI
- 🧠 LangGraph memory for threaded conversations

---

## 🗂️ Project Structure

```
Multi_Agents/
├── .env
├── .gitignore
├── langgraph.json
├── main.py
├── graph.py
├── llm_init.py
├── nodes.py
├── state.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── chatbot_agent/
│   │   │   ├── __init__.py
│   │   │   └── chatbot.py
│   │   ├── flight_agent/
│   │   │   ├── __init__.py
│   │   │   ├── flight_agent.py
│   │   │   └── flight_tool.py
│   │   └── itinerary_agent/
│   │       ├── __init__.py
│   │       └── itinerary_agent.py
```

---

## .env Configuration

```env
GOOGLE_API_KEY=your_google_key
TAVILY_API_KEY=your_tavily_key
RAPIDAPI_KEY=your_rapidapi_key
```

---

## 🚀 How to Run

### ▶️ CLI Mode
```bash
python main.py
```

### 💻 Streamlit Web App
```bash
streamlit run streamlit_app.py
```

---

## 📦 Requirements

All dependencies are listed in `requirements.txt`.

---

## 💡 Agents Logic

- **Chatbot Agent**: Routes based on intent and data completeness
- **Flight Agent**: Uses `flight_tool` to query RapidAPI
- **Itinerary Agent**: Builds markdown travel guides with budgeting and tips

---

## 📌 Built With

- LangGraph
- LangChain
- Streamlit
- RapidAPI (Flight Search)

---

Your AI-powered travel sidekick. Smart, fast, and budget-friendly ✈️💼
