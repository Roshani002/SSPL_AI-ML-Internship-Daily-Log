import streamlit as st
import uuid
from langchain_core.messages import AIMessage, HumanMessage
from graph import graph

st.set_page_config(
    page_title="TravelBot",
    page_icon="✈️",
    layout="centered"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .main .block-container { max-width: 800px; padding-top: 2rem; padding-bottom: 2rem; }
    h1 { font-weight: 600; color: #fafafa; }
    .st-emotion-cache-16idsys p { color: #a0a0a0; }
    [data-testid="chat-message-container"] { border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    [data-testid="chat-message-container"]:has([data-testid="stChatMessageContent-assistant"]) { background-color: #262730; }
    [data-testid="chat-message-container"]:has([data-testid="stChatMessageContent-user"]) { background-color: #4f46e5; }
    [data-testid="stChatInput"] { background-color: #0e1117; }
    [data-testid="stChatInput"] > div { background-color: #262730; }
</style>
""", unsafe_allow_html=True)


st.title("✈️ TravelBot")
st.caption("Your AI-powered travel planning assistant. You can ask for flights or to plan an itinerary.")


# --- Session State Initialization ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = [
        AIMessage(content="Hello! I'm TravelBot. How can I help you plan your trip today?")
    ]

# The config is crucial for the graph to remember conversation history
config = {"configurable": {"thread_id": st.session_state.thread_id}}

# --- Function to handle message processing and display ---
def process_and_display_messages():
    # Render all messages in the session state
    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            st.chat_message("assistant", avatar="🤖").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user", avatar="😊").write(msg.content)

# --- Display existing chat history ---
process_and_display_messages()

# --- Handle New User Input ---
if prompt := st.chat_input("Ask about flights or an itinerary..."):
    # Add user message to session state
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Display the user's message immediately
    st.chat_message("user", avatar="😊").write(prompt)

    # Use a spinner while the graph is running
    with st.spinner("Thinking..."):
        processed_contents = set()
        # The input to the graph is just the new message.
        # The checkpointer (memory) is responsible for loading the history.
        events = graph.stream(
            {"messages": [HumanMessage(content=prompt)]}, config=config
        )
        
        # This list will hold the new AI messages from this turn
        # new_ai_messages = []
        
        # Process every event from the stream
        for event in events:
            for node_name, node_state in event.items():
                # We are only interested in nodes that add messages
                if "messages" not in node_state or not node_state["messages"]:
                    continue

                last_message = node_state["messages"][-1]
                
                # Check if this is a new, valid AIMessage we should display
                if isinstance(last_message, AIMessage) and last_message.content:
                    if last_message.content not in processed_contents:
                        # Display the new message
                        st.chat_message("assistant", avatar="🤖").write(last_message.content)
                        # Add it to the session history
                        st.session_state.messages.append(last_message)
                                # Mark its content as processed for this turn
                        processed_contents.add(last_message.content)
                    # Avoid adding duplicate messages
        #             if not new_ai_messages or new_ai_messages[-1].content != last_message.content:
        #                 new_ai_messages.append(last_message)

        # # After the stream is complete, display each new AI message and add to session state
        # for msg in new_ai_messages:
        #     st.session_state.messages.append(msg)
        #     st.chat_message("assistant", avatar="🤖").write(msg.content)