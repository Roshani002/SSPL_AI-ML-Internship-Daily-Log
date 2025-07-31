# main.py

from graph import graph
import uuid
from langchain_core.messages import AIMessage

if __name__ == "__main__":
    conversation_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": conversation_id}}

    print("Chatbot: Hello! I'm TravelBot. How can I help you plan your trip today?")
    print("         You can ask for flights or to plan an itinerary. Type 'quit' to exit.")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                break

            for event in graph.stream({"messages": [("user", user_input)]}, config=config):
                # The event dictionary's keys are the names of the nodes that just ran.
                for node_name, node_state in event.items():
                    # printing messages from the AI.
                    if "messages" in node_state and node_state["messages"]:
                        last_message = node_state["messages"][-1]
                        
                        # If the last message is an AIMessage with content, print it.
                        if isinstance(last_message, AIMessage) and last_message.content:

                            if node_name in ["flight_agent", "itinerary_agent"]:
                                print(f"\n--- TravelBot's Response ---")
                                print(last_message.content)
                                print("----------------------------\n")
                            else:
                                print(f"Chatbot: {last_message.content}")

        except KeyboardInterrupt:
            print("\nChatbot: Goodbye!")
            break