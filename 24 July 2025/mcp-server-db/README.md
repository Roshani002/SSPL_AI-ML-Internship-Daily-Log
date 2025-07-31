# 🧠 MCP Database Server with CLI Chat

This project implements a fully functional CLI chatbot agent backed by an SQLite database and MCP (Modular Context Protocol). It uses `mcp-server`, `mcp-use`, and `Groq LLM` to perform dynamic tool calls like:

- ✅ Fetching recent users
- ✅ Filtering users by department, role, and active status
- ✅ Creating users with validations
- ✅ Transferring users across departments with audit logs

---

## 📦 Features

- ✅ CLI Chat interface powered by `Groq` and LangChain
- ✅ Live connection to multiple MCP servers
- ✅ SQLite backend with auto-populated user data and audit logs
- ✅ Robust tool registration using `pydantic` schemas
- ✅ Fully asynchronous with graceful error handling and logs

---

## 🗂 Project Structure

```
.
├── main.py               # CLI chatbot entry point
├── client.py             # MCPClient logic (tool selection + Groq integration)
├── server.py             # MCP server: registers tools/resources + DB handlers
├── database.py           # Async DB logic (init, schema, insert)
├── users.py              # Tool handlers (create, transfer)
├── constants.py          # Global constants (prompts, config path)
├── mcp.json              # Defines stdio servers for CLI to connect
├── pyproject.toml        # Project config
├── .env                  # API keys and DB path
```

---

## 🔐 Environment (.env)

```env
CLIENT_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your_groq_api_key
DB_PATH=company.db
```

---

## 🧪 How to Run

### 1. Start the MCP server:
```bash
python server.py
```

### 2. Start the CLI chat:
```bash
python main.py
```

---

## 🔧 Tools Registered

- `create_user`
- `transfer_user`
- `get_recent_users`
- `get_users_by_criteria`

---

## 🧠 LLM + Tool Reasoning

This project shows how to connect an LLM (Groq) to real-world tools and databases, giving it the power to use `structured outputs` to make decisions and call functions based on input.

Ready to deploy into a real backend, agent framework, or API layer.

