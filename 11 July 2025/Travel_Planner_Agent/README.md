# 🌍 Travel Planner Agent (CrewAI + Streamlit)

This project is a smart travel planner that generates customized, multi-agent travel guides using CrewAI and Streamlit. It fetches real-time info using Tavily, combines insights from multiple travel experts (agents), and outputs everything in a well-structured markdown format via an interactive Streamlit app or terminal.

---

## 🧳 Features

- 🌐 Real-time search with Tavily
- 🧠 Multi-agent system:
  - **Destination Researcher**
  - **Attractions Specialist**
  - **Local Guide**
- 🪄 Sequential task processing for clean results
- 📄 Markdown-formatted output for easy reading
- 🌞 Forecast-based and budget-aware suggestions

---

## 📂 File Structure

```
TRAVEL_PLANNER_AGENT/
├── .env
├── .gitignore
├── main.py
├── streamlit_app.py
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agents.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   └── tasks_updated.py
│   └── tools/
│       ├── __init__.py
│       └── custom_tool.py

```

---

## ⚙️ Environment Setup

Create a `.env` file with the following:

```env
MODEL=gemini/gemini-2.0-flash
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
```

---

## 🚀 Running the App

**Option 1: Command Line**

```bash
python main.py
```

**Option 2: Streamlit Web UI**

```bash
streamlit run streamlit_app.py
```

---


---

