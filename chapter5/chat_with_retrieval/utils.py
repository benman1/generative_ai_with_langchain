"""Utility functions and constants.

I am having some problems caching the memory and the retrieval. When
I decorate for caching, I get streamlit init errors.
"""

import logging
import pathlib
from typing import Any

from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders.epub import UnstructuredEPubLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_core.documents import Document
from streamlit.logger import get_logger

logging.basicConfig(encoding="utf-8", level=logging.INFO)
LOGGER = get_logger(__name__)


def init_memory():
    """Initialize the memory for contextual conversation.

    We are caching this, so it won't be deleted
     every time, we restart the server.
    """
    return ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, output_key="answer"
    )


LOGGER.info("init memory")
MEMORY = init_memory()


class EpubReader(UnstructuredEPubLoader):
    def __init__(self, file_path: str | list[str], **unstructured_kwargs: Any):
        super().__init__(file_path, **unstructured_kwargs, mode="elements", strategy="fast")


class DocumentLoaderException(Exception):
    pass


class DocumentLoader(object):
    """Loads in a document with a supported extension."""

    supported_extensions = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".epub": EpubReader,
        ".docx": UnstructuredWordDocumentLoader,
        ".doc": UnstructuredWordDocumentLoader,
    }


def load_document(temp_filepath: str) -> list[Document]:
    """Load a file and return it as a list of documents.

    Doesn't handle a lot of errors at the moment.
    """
    ext = pathlib.Path(temp_filepath).suffix
    loader = DocumentLoader.supported_extensions.get(ext)
    if not loader:
        raise DocumentLoaderException(
            f"Invalid extension type {ext}, cannot load this type of file"
        )

    loaded = loader(temp_filepath)
    docs = loaded.load()
    logging.info(docs)
    return docs
