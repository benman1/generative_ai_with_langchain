"""Chat with retrieval and embeddings.

Run like this:
> PYTHONPATH=. streamlit run chat_with_retrieval/chat_with_documents.py
"""
import os
import tempfile
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import OpenAIModerationChain, SimpleSequentialChain

from chat_with_retrieval.utils import (
    load_document, DocumentLoader,
    configure_retriever,
    configure_chain
)

st.set_page_config(page_title="LangChain: Chat with Documents", page_icon="🦜")
st.title("🦜 LangChain: Chat with Documents")


def configure_retrieval_chain(
        uploaded_files,
        use_compression: bool = False,
        use_flare: bool = False,
        use_moderation: bool = False
):
    """Read documents, configure retriever, and the chain."""
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
        docs.extend(load_document(temp_filepath))

    retriever = configure_retriever(docs=docs, use_compression=use_compression)
    chain = configure_chain(retriever=retriever, use_flare=use_flare)
    if not use_moderation:
        return chain

    moderation_chain = OpenAIModerationChain()
    return SimpleSequentialChain(chains=[chain, moderation_chain])


uploaded_files = st.sidebar.file_uploader(
    label="Upload files",
    type=list(DocumentLoader.supported_extentions.keys()),
    accept_multiple_files=True
)
if not uploaded_files:
    st.info("Please upload documents to continue.")
    st.stop()

# use compression by default:
use_compression = st.checkbox("compression", value=True)
use_flare = st.checkbox("flare", value=True)
use_moderation = st.checkbox("moderation", value=False)

user_query = st.chat_input(placeholder="Ask me anything!")
assistant = st.chat_message("assistant")

CONV_CHAIN = configure_retrieval_chain(
    uploaded_files,
    use_compression=use_compression,
    use_flare=use_flare,
    use_moderation=use_moderation
)

if user_query:
    stream_handler = StreamlitCallbackHandler(assistant)
    response = CONV_CHAIN.run(user_query, callbacks=[stream_handler])
    st.markdown(response)
