"""Shared code for the semantic search."""
from langchain.embeddings import OpenAIEmbeddings

get_embeddings = OpenAIEmbeddings
# alternatively, for local embeddings, use:
# from functools import partial
# from langchain.embeddings import HuggingFaceEmbeddings
# embeddings = lambda: partial(HuggingFaceEmbeddings,
#   model_name="multi-qa-mpnet-base-dot-v1"
# )
INDEX_PATH = "faiss_index.db"
