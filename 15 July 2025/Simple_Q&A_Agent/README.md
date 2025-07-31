# 🤖 Simple Q&A Agent with LangChain

This project demonstrates how to build a simple Q&A conversational agent using LangChain. It integrates tools like Tavily for internet search and Groq for LLM execution, while enabling tracing through LangSmith.

---

## 📚 Key Features

- Built with [LangChain](https://www.langchain.com/)
- Internet search via **Tavily**
- LLM support via **Groq**
- Integrated LangSmith for tracing and project tracking
- Notebook-based development (`.ipynb`) for experimentation

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following keys:

```env
LANGSMITH_TRACING=True
LANGSMITH_PROJECT=my_first_agent
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_key
TAVILY_API_KEY=your_tavily_key
GROQ_API_KEY=your_groq_key
```

---

