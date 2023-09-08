"""Document indexing.

Building a vector store fast.

Adapted from open_source_LLM_search_engine:
https://github.com/ray-project/langchain-ray/

Please note that there are FAISS versions for processing on
either CPU or GPU, which can be installed like this:
>> pip install faiss-gpu # For CUDA 7.5+ Supported GPU's.
# OR
>> pip install faiss-cpu # For CPU Installation

"""
import time

import numpy as np
import ray
from bs4 import BeautifulSoup as Soup
from langchain import FAISS
from langchain.document_loaders import RecursiveUrlLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import set_environment
from search_engine.utils import INDEX_PATH, get_embeddings

# set keys:
set_environment()


def chunk_docs(url: str) -> list[Document]:
    """Crawl a website and chunk the text in it.

    Wrapping the texts into list[Document] in
    order to keep the metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter()

    # Load docs
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=2,
        extractor=lambda x: Soup(x, "html.parser").text
    )
    docs = loader.load()

    # Split into sentences.
    return text_splitter.create_documents(
        [doc.page_content for doc in docs],
        metadatas=[doc.metadata for doc in docs]
    )


def create_db(chunks: list[Document]) -> FAISS:
    """This is the easy way."""
    return FAISS.from_documents(
        chunks,
        OpenAIEmbeddings()
        # get_embeddings()
    )


@ray.remote
def process_shard(chunks: list[Document]):
    """Process task.

    You can specify the number of GPUs or CPUs you want to use as
    part of the ray decorator.
    """
    return FAISS.from_documents(
        documents=chunks,
        embedding=get_embeddings()
    )


def create_db_parallel(chunks: list[Document]):
    """Create a FAISS db with parallelism."""
    # Split chunks into shards:
    shards = np.array_split(chunks, 8)

    # Start Ray
    ray.init()

    # Process shards in parallel:
    futures = [process_shard.remote(shard) for shard in shards]
    results = ray.get(futures)

    # Merge index shards
    db = results[0]
    for result in results[1:]:
        db.merge_from(result)

    # Shut down Ray:
    ray.shutdown()
    return db


if __name__ == "__main__":
    print("Starting indexing process.")
    st = time.time()
    chunks = chunk_docs(url="https://docs.ray.io/en/latest/")
    if len(chunks) == 0:
        raise ValueError("No chunks created!")
    db = create_db(chunks)  # create_db_parallel(chunks)
    db.save_local(INDEX_PATH)
    et = time.time() - st
    print(f"Completed in {et} seconds.")
    """
    Starting indexing process.
    Completed in 30.39633297920227 seconds.
    """
