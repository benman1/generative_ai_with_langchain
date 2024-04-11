"""Chat with retrieval and embeddings."""

import os
import tempfile

from langchain.chains.base import Chain
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chains.flare.base import FlareChain
from langchain.chains.moderation import OpenAIModerationChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chat_with_retrieval.utils import MEMORY, load_document, LOGGER
from config import set_environment


set_environment()

LOGGER.info("setup LLM")
# Setup LLM and QA chain; set temperature low to keep hallucinations in check
LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)


LOGGER.info("configure_retriever")


def configure_retriever(docs: list[Document], use_compression: bool = False) -> BaseRetriever:
    """Retriever to use."""
    # Split each document documents:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create embeddings and store in vectordb:
    embeddings = OpenAIEmbeddings()
    # alternatively: HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Create vectordb with single call to embedding model for texts:
    vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 7, "include_metadata": True},
    )
    if not use_compression:
        return retriever

    embeddings_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.2)
    return ContextualCompressionRetriever(
        base_compressor=embeddings_filter,
        base_retriever=retriever,
    )


def configure_chain(retriever: BaseRetriever, use_flare: bool = True) -> Chain:
    """Configure chain with a retriever.

    Passing in a max_tokens_limit amount automatically
    truncates the tokens when prompting your llm!
    """
    output_key = 'response' if use_flare else 'answer'
    MEMORY.output_key = output_key
    params = dict(
        llm=LLM,
        retriever=retriever,
        memory=MEMORY,
        verbose=True,
        max_tokens_limit=4000,
    )
    if use_flare:
        # different set of parameters and init
        return FlareChain.from_llm(**params)
    return ConversationalRetrievalChain.from_llm(**params)


def configure_retrieval_chain(
    uploaded_files,
    use_compression: bool = False,
    use_flare: bool = False,
    use_moderation: bool = False,
) -> Chain:
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
