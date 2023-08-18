"""Chat with retrieval and embeddings.

Run like this:
> PYTHONPATH=. streamlit run chat_with_retrieval/chat_with_documents.py
"""
import os

import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

from chat_with_retrieval.app import configure_retrieval_chain
from chat_with_retrieval.utils import MEMORY, DocumentLoader

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


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container.expander("Context Retrieval")

    def on_retriever_start(self, query: str, **kwargs):
        self.container.write(f"**Question:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.container.write(f"**Document {idx} from {source}**")
            self.container.markdown(doc.page_content)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)
