"""Document indexing.

Building a vector store fast.

Adapted from open_source_LLM_search_engine:
https://github.com/ray-project/langchain-ray/
"""
import time

import requests
from fastapi import FastAPI
from langchain import FAISS
from ray import serve

from config import set_environment
from search_engine.utils import INDEX_PATH, get_embeddings

# set keys:
set_environment()

app = FastAPI()


@serve.deployment(route_prefix="/")
@serve.ingress(app)
class VectorSearchDeployment:
    def __init__(self):
        # Load the data from faiss
        st = time.time()
        self.embeddings = get_embeddings()
        self.db = FAISS.load_local(INDEX_PATH, self.embeddings)
        et = time.time() - st
        print(f"Loading database took {et} seconds.")

    @app.get("/search")
    def search(self, query: str):
        results = self.db.max_marginal_relevance_search(query, k=1, fetch_k=10)
        retval = ""
        for i in range(len(results)):
            chunk = results[i]
            source = chunk.metadata["source"]
            retval = retval + f"From http://{source}\n\n"
            retval = retval + chunk.page_content
            retval = retval + "\n====\n\n"

        return retval


if __name__ == "__main__":
    # using bind() instead of remote()
    # this will ready the dag, but not execute it yet.
    app = VectorSearchDeployment.bind()
    serve.run(app)
    print(requests.get(
        "http://localhost:8000/search",
        params={
            "query": "What are the different components of Ray"
                     " and how can they help with large language models (LLMs)?"
        }
    ).json())
