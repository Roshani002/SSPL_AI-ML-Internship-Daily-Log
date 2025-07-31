# 🧠 Research Agent (CrewAI + Streamlit)

A fully autonomous research assistant built using [CrewAI](https://docs.crewai.com/) and [Streamlit], powered by OpenRouter and Tavily. Just enter a topic, and this agent digs up recent advancements and summarizes them into an insightful, concise report — all within a clean web interface.

---

## 🗂️ Project Structure

```
.
├── main.py                # Streamlit app UI
├── src/
│   ├── agents/
│   │   └── agent.py       # CrewAI Agent definition
│   ├── tasks/
│   │   └── task.py        # Task creation for the agent
│   └── tools/
│       └── tool.py        # Tavily search tool integration
├── .env                   # Your API keys (not checked into version control)
```

---

## 🧪 Features

- ✅ Autonomous agent using `CrewAI`
- ✅ Real-time internet search with `Tavily`
- ✅ Visual streaming of agent activity with `Streamlit`
- ✅ Modular and extensible design

---

## 🔐 Setup: Create `.env`

Before running, create a `.env` file at the root of your project with the following keys:

```env
MODEL=openrouter/deepseek/deepseek-r1-0528:free
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit app
streamlit run main.py
```

---


