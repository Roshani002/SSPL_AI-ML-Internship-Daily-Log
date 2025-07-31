# """The module runs a CLI ChatBot that uses groqclient
# """

# import json
# from dataclasses import dataclass
# from server.constants import (
#     SERVER_CONFIG_PATH,
#     CLI_CLIENT_SYSTEM_PROMPT,
#     CLI_CLIENT_STOP_WORDS,
# )
# from server.client import MCPClient


# @dataclass
# class ServerConfig:
#     stdio_servers: list[str]

#     def list_servers(self):
#         return self.stdio_servers + self.stdio_servers


# async def main():
#     with open(SERVER_CONFIG_PATH, "r") as file:
#         data = json.load(file)

#     server_config = ServerConfig(**data)

#     client = MCPClient()

#     for i, server in enumerate(server_config.stdio_servers):
#         await client.connect_to_stdio_server("stdio" + str(i), server)

    
#     messages = [
#         {
#             "role": "system",
#             "content": CLI_CLIENT_SYSTEM_PROMPT,
#         }
#     ]

#     print("Welcome to the CLI chat bot. You can type stop to exit.")

#     while True:
#         user_input = input("User: ").strip()

#         if user_input.lower() in CLI_CLIENT_STOP_WORDS:
#             print("Exiting chat...")
#             break

#         messages = await client.process_query(messages, user_input)

#         # Assume last message is the assistant's response
#         assistant_message = messages[-1]

#         print(10 * "-", "Assistant", 10 * "-")
#         print(assistant_message["content"])
#         print(30 * "-")

#         if len(messages) > 5:
#             messages = messages[-5:]

#     # Close connection
#     await client.exit_stack.aclose()


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())

# # TODO:
# # refactor the code
# # use groq agent


"""The module runs a CLI ChatBot that uses groqclient
"""

import json
import os
from dataclasses import dataclass
from Server.constants import (
    SERVER_CONFIG_PATH,
    CLI_CLIENT_SYSTEM_PROMPT,
    CLI_CLIENT_STOP_WORDS,
)
from Server.client import MCPClient


@dataclass
class ServerConfig:
    stdio_servers: list[str]

    def list_servers(self):
        return self.stdio_servers + self.stdio_servers


async def main():
    # Check if config file exists
    if not os.path.exists(SERVER_CONFIG_PATH):
        print(f"Error: Configuration file not found at {SERVER_CONFIG_PATH}")
        print(f"Current working directory: {os.getcwd()}")
        print("Please make sure the mcp.json file exists in the correct location.")
        return

    try:
        with open(SERVER_CONFIG_PATH, "r") as file:
            content = file.read().strip()
            if not content:
                print(f"Error: Configuration file {SERVER_CONFIG_PATH} is empty")
                return
            data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {SERVER_CONFIG_PATH}: {e}")
        print("Please check that your mcp.json file has valid JSON format")
        return
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return

    # Validate required fields
    if "stdio_servers" not in data:
        print("Error: 'stdio_servers' field not found in configuration")
        print("Expected format: {'stdio_servers': ['path/to/server.py']}")
        return

    server_config = ServerConfig(**data)

    if not server_config.stdio_servers:
        print("Error: No servers configured in stdio_servers array")
        return

    client = MCPClient()

    # Connect to servers
    connected_servers = 0
    for i, server in enumerate(server_config.stdio_servers):
        server_id = "stdio" + str(i)
        print(f"Attempting to connect to server: {server}")
        
        if not os.path.exists(server):
            print(f"Warning: Server file not found: {server}")
            continue
            
        try:
            await client.connect_to_stdio_server(server_id, server)
            connected_servers += 1
            print(f"Successfully connected to {server}")
        except Exception as e:
            print(f"Failed to connect to server {server}: {e}")

    if connected_servers == 0:
        print("Error: No servers connected successfully")
        return

    messages = [
        {
            "role": "system",
            "content": CLI_CLIENT_SYSTEM_PROMPT,
        }
    ]

    print(f"\nWelcome to the CLI chat bot. Connected to {connected_servers} server(s).")
    print("You can type 'stop', 'exit', or 'quit' to exit.")

    while True:
        try:
            user_input = input("\nUser: ").strip()

            if user_input.lower() in CLI_CLIENT_STOP_WORDS:
                print("Exiting chat...")
                break

            if not user_input:
                continue

            messages = await client.process_query(messages, user_input)

            # Assume last message is the assistant's response
            assistant_message = messages[-1]

            print(10 * "-", "Assistant", 10 * "-")
            print(assistant_message["content"])
            print(30 * "-")

            if len(messages) > 5:
                messages = messages[-5:]

        except KeyboardInterrupt:
            print("\nExiting chat...")
            break
        except Exception as e:
            print(f"Error processing query: {e}")

    # Close connection
    try:
        await client.exit_stack.aclose()
        print("Connections closed successfully")
    except Exception as e:
        print(f"Error closing connections: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())