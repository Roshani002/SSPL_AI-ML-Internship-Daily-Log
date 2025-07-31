import os
import json
import asyncio
from typing import Dict
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from groq import Groq
from dotenv import load_dotenv
from Server.constants import TOOL_RESPONSE_LIMIT

load_dotenv()

# Groq client
CLIENT_MODEL = os.environ.get("CLIENT_MODEL", "llama-3.1-8b-instant")
print(f"Using {CLIENT_MODEL = }")

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self.groq_client = Groq()
        self.available_tools = []
        self.mcp_servers = {}

    # methods
    async def connect_to_stdio_server(self, server_id: str, server_script_path: str):
        """Connect to an MCP server and store the session using a custom server ID

        Args:
            server_id: Unique identifier for the server (e.g., script path or custom name)
            server_script_path: Path to the server script (.py)
        """
        is_python = server_script_path.endswith('.py')
        if not os.path.exists(server_script_path):
                raise FileNotFoundError(f"Server script not found: {server_script_path}")
            
        if not is_python:
            raise ValueError("Server script must be a .py file")

        # Get absolute path
        abs_path = os.path.abspath(server_script_path)
        print(f"Connecting to server at: {abs_path}")

        command = "python" if is_python else None
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))

        await session.initialize()

        # List available tools
        response = await session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

        # Store the session in the dictionary using the server_id
        self.sessions[server_id] = session

        # Update the available tools and servers
        await self._get_available_tools()
    
    async def interact_with_server(self, server_id: str, action: str):
        """Interact with a specific server using its ID

        Args:
            server_id: Unique identifier for the server
            action: The action you want to perform with the selected server
        """
        if server_id not in self.sessions:
            raise ValueError(f"Server with ID {server_id} not found")

        session = self.sessions[server_id]

        # Example action: Listing tools (can be extended for other actions)
        if action == "list_tools":
            response = await session.list_tools()
            tools = response.tools
            print(
                f"Tools available on server {server_id}:", [tool.name for tool in tools]
            )

    async def close_all_connections(self):
        """Close all active server connections."""
        for server_id, session in self.sessions.items():
            # await session.closeGracefully()
            print(f"Closed connection for server {server_id}")

        # Ensure all resources are properly cleaned up
        await self.exit_stack.aclose()
    
    async def _get_available_tools(self):
        # fetch the lost of available tools in MCP servers
        self.available_tools = []   # Reset tools list
        for server_name, session in self.sessions.items():
            response = await session.list_tools()
            self.available_tools.extend(
                [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description if tool.description else "",
                            "parameters": tool.inputSchema,
                        },
                    }
                    for tool in response.tools
                ]
            )
            self.mcp_servers[server_name] = [tool.name for tool in response.tools]

    async def process_query(self, messages: list, query: str) -> list:
        """Process a query using Groq and available tools"""
        messages.append({"role": "user", "content": query})

        if not self.mcp_servers:
            raise ValueError("No MCP servers found")

        # LLM call - can choose the tool to use
        response = self.groq_client.chat.completions.create(
            model=CLIENT_MODEL,
            messages=messages,
            tools=self.available_tools,
            tool_choice="auto",
            max_completion_tokens=4096,
        )

        choice = response.choices[0]

        if choice.finish_reason == "tool_calls":
            tool_calls = choice.message.model_dump()["tool_calls"]
            # record the tool calls
            messages.append({"role": "assistant", "content": str(tool_calls)})

            # Extract and print function name and arguments
            print(
                "\n".join(
                    [
                        f"Tool Call: {c['function']['name']},"
                        + f" Args: {c['function']['arguments']}"
                        for c in tool_calls
                    ]
                )
            )

            # LLM can decide to use multiple tools
            for tool in tool_calls:

                server = None
                # find the server that has the selected tool
                for server_name, tool_lst in self.mcp_servers.items():
                    if tool["function"]["name"] in tool_lst:
                        server = server_name
                        break

                if not server:
                    raise ValueError(
                        f"Server for tool {tool['function']['name']} not found"
                    )

                # tool call
                response = await self.sessions[server].call_tool(
                    tool["function"]["name"], json.loads(tool["function"]["arguments"])
                )
                messages.append(
                    {
                        "role": "tool",
                        "content": str(response.model_dump()["content"])[
                            :TOOL_RESPONSE_LIMIT
                        ],
                        "tool_call_id": tool["id"],
                    }
                )

                print(
                    f"Tool {tool['id']} response (truncated):",
                    {str(response.model_dump()["content"])[:TOOL_RESPONSE_LIMIT]},
                )

                # LLM call - synthesize the final response based on the tool's response
                response = self.groq_client.chat.completions.create(
                    model=CLIENT_MODEL,
                    messages=messages,
                    max_completion_tokens=4096,
                )
                # record assistant response
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
                    }
                )
        else:
            # final response if tool use is not required
            messages.append({"role": "assistant", "content": choice.message.content})

        return messages