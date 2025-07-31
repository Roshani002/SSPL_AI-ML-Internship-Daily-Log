# Chatbot Agent with Memory & Human-in-the-Loop

A simple chatbot agent built with [LangGraph](https://github.com/langgraph/langgraph) and LangChain, featuring:

- **Persistent memory** via `MemorySaver`
- **Human-in-the-loop** clarification using `interrupt` + `ask_user_for_clarification` tool
- **External search** integration (TavilySearch)
- Runs locally in VSCode **and** in LangGraph Studio UI

---

## 📁 Project Structure

```
Chatbot_Agent/
├── .dockerignore
├── .gitignore
├── .README.md
├── .env                 # Your API keys 
├── langgraph.json       # Langgraph config which specifies the dependencies, graphs, environment variables
├── venv/                # Python virtual environment
├── .langgraph_api/      # LangGraph Studio cache (auto-created by langgraph dev command)
└── agent/
    ├── __init__.py
    ├── agent.py         # Graph definition & runtime
    └── utils/
        ├── __init__.py
        ├── nodes.py     # ToolNode wiring
        ├── state.py     # State schema
        └── tools.py     # tools
```

---

## 🛠️ Prerequisites

- Python 3.10+
- langchain
- langchain-tavily
- langchain-core
- langchain-community
- langchain-google-genai
- langgraph
- langgraph-cli[inmem]
- ipython
- python-dotenv

---


## 🔧 Configuration

Create a file named `.env` in the project root:

```ini
GOOGLE_API_KEY=<your-google-gemini-key>
TAVILY_API_KEY=<your-tavily-api-key>
LANGSMITH_API_KEY=<your-langsmith-key>
```

---

## 🌐 Running in LangGraph Studio
Follow steps: https://langchain-ai.lang.chat/langgraph/tutorials/langgraph-platform/local-server/

---

## 🔍 How It Works

- **Memory**  
  Uses `MemorySaver` to persist conversation history across sessions.

- **Human-in-the-Loop**  
  If the AI needs more detail, it triggers an `interrupt` and calls `ask_user_for_clarification`, pausing until you reply.

- **Tools**  
  - **TavilySearch**: external web/search queries  
  - **ask_user_for_clarification**: targeted follow-up questions  

---

