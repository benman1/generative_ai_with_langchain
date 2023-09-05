"""Document loading functionality.

Run like this:
> PYTHONPATH=. streamlit run chat_with_retrieval/chat_with_documents.py
"""
import logging

import streamlit as st
from streamlit.external.langchain import StreamlitCallbackHandler

from chat_with_retrieval.chat_with_documents import configure_retrieval_chain
from chat_with_retrieval.utils import MEMORY, DocumentLoader

logging.basicConfig(encoding="utf-8", level=logging.INFO)
LOGGER = logging.getLogger()

st.set_page_config(page_title="LangChain: Chat with Documents", page_icon="🦜")
st.title("🦜 LangChain: Chat with Documents")


uploaded_files = st.sidebar.file_uploader(
    label="Upload files",
    type=list(DocumentLoader.supported_extensions.keys()),
    accept_multiple_files=True
)
if not uploaded_files:
    st.info("Please upload documents to continue.")
    st.stop()

# use compression by default:
use_compression = st.checkbox("compression", value=False)
use_flare = st.checkbox("flare", value=False)
use_moderation = st.checkbox("moderation", value=False)

CONV_CHAIN = configure_retrieval_chain(
    uploaded_files,
    use_compression=use_compression,
    use_flare=use_flare,
    use_moderation=use_moderation
)

if st.sidebar.button("Clear message history"):
    MEMORY.chat_memory.clear()

avatars = {"human": "user", "ai": "assistant"}
for msg in MEMORY.chat_memory.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

assistant = st.chat_message("assistant")
if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)
    stream_handler = StreamlitCallbackHandler(assistant)
    with st.chat_message("assistant"):
        response = CONV_CHAIN.run({
            "question": user_query,
            "chat_history": MEMORY.chat_memory.messages
        }, callbacks=[stream_handler]
        )
