"""Document loading functionality."""
import logging
import os
import pathlib
from typing import Any
import streamlit as st

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain, FlareChain
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import (
    PyPDFLoader, UnstructuredEPubLoader,
    UnstructuredWordDocumentLoader, TextLoader
)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.schema import Document, BaseRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch

from config import set_environment

logging.basicConfig(encoding="utf-8", level=logging.INFO)
LOGGER = logging.getLogger()
set_environment()
# Setup LLM and QA chain; set temperature low to keep hallucinations in check
LLM = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, streaming=True
)


@st.cache_resource
def init_memory():
    """Initialize the memory for contextual conversation.

    We are caching this, so it won't be deleted
     every time, we restart the server.
     """
    return ConversationBufferMemory(
        llm=LLM,
        return_messages=True
    )

class EpubReader(UnstructuredEPubLoader):
    def __init__(self, file_path: str | list[str], **unstructured_kwargs: Any):
        super().__init__(file_path, **unstructured_kwargs, mode="elements", strategy="fast")


class DocumentLoaderException(Exception):
    pass


class DocumentLoader(object):
    """Loads in a document with a supported extension."""
    supported_extentions = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".epub": EpubReader,
        ".docx": UnstructuredWordDocumentLoader,
        ".doc": UnstructuredWordDocumentLoader
    }


def load_document(temp_filepath: str) -> list[Document]:
    """Load a file and return it as a list of documents.

    Doesn't handle a lot of errors at the moment.
    """
    ext = pathlib.Path(temp_filepath).suffix
    loader = DocumentLoader.supported_extentions.get(ext)
    if not loader:
        raise DocumentLoaderException(
            f"Invalid extension type {ext}, cannot load this type of file"
        )

    loader = loader(temp_filepath)
    docs = loader.load()
    logging.info(docs)
    return docs


def configure_retriever(
        docs: list[Document],
        use_compression: bool = False
) -> BaseRetriever:
    """Retriever to use."""
    # Split each document documents:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create embeddings and store in vectordb:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Create vectordb with single call to embedding model for texts:
    vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)
    retriever = vectordb.as_retriever(
        search_type="mmr", search_kwargs={
            "k": 2,
            "fetch_k": 4,
            "include_metadata": True
        },
    )
    if not use_compression:
        return retriever

    embeddings_filter = EmbeddingsFilter(
        embeddings=embeddings, similarity_threshold=0.2
    )
    return ContextualCompressionRetriever(
        base_compressor=embeddings_filter,
        base_retriever=retriever,
    )


def configure_chain(retriever: BaseRetriever, use_flare: bool = True) -> Chain:
    """Configure chain with a retriever.

    Passing in a max_tokens_limit amount automatically
    truncates the tokens when prompting your llm!
    """
    chain = FlareChain if use_flare else ConversationalRetrievalChain
    return chain.from_llm(
        LLM,
        retriever=retriever,
        memory=init_memory(),
        verbose=True,
        max_tokens_limit=4000,
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
