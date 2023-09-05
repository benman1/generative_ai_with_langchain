"""Utility functions and classes."""
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder


def init_memory():
    """Initialize the memory for contextual conversation.

    We are caching this, so it won't be deleted
     every time, we restart the server.
     """
    return ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )


MEMORY = init_memory()
CHAT_HISTORY = MessagesPlaceholder(variable_name="chat_history")
