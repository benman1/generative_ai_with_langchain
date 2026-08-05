# Chapter 4 - Retrieval Augmented Generation

Code for chapter 4 of *Generative AI with LangChain*, third edition.

Targets **LangChain v1** (`langchain>=1.3`, `langgraph>=1.2`). This is not the
second edition's 0.3 line, and the differences break code rather than warn about
it: `langchain.retrievers` and `langchain.chains` no longer exist, and what lived
there now ships in the separate `langchain-classic` package, which
`pip install langchain` does not pull in.

## Setup

```bash
pip install -r requirements.txt
python build_corpus.py          # once; builds data/japan_corpus.json
```

**No paid API key is needed.** Embeddings are a static CPU model, the reranker is
a local cross-encoder, and the one step that wants a chat model falls back to a
fixed plan when `OPENAI_API_KEY` is unset, so every notebook runs top to bottom
offline. Set the key to see the drafting step do real work.

## Notebooks

| Notebook | What it covers | Book section |
|---|---|---|
| [01_embeddings_and_vectorstores.ipynb](01_embeddings_and_vectorstores.ipynb) | Embedding text, storing vectors, the vector store interface | *Transformers and vector spaces*, *Vector stores and databases* |
| [02_document_processing.ipynb](02_document_processing.ipynb) | Loading documents and the chunking strategies | *Document processing* |
| [03_retrieval.ipynb](03_retrieval.ipynb) | Reciprocal rank fusion, hybrid retrieval, presets, indexing in levels, citation and groundedness checks, and the measurements behind Figure 4.3 | *Reranking and hybrid search*, *Advanced retrieval* |
| [04_itinerary_assistant.ipynb](04_itinerary_assistant.ipynb) | The four retrieval sources, the distance matrix, the typed plan, the code validator, the LangGraph loop with a human pause, learning from edits, and the backtest | *Building an itinerary assistant* |

Every numbered listing in the chapter is a cell in one of these. The two new
notebooks are committed with their outputs, so you can read the numbers without
running anything.

## Modules

| File | Role |
|---|---|
| `wikivoyage.py` | Parses Wikivoyage articles into prose sections **and** structured places with coordinates. A parser that strips the `{{see}}` / `{{do}}` / `{{sleep}}` templates as markup deletes every place name and coordinate in the corpus; the chapter measures what that costs. |
| `build_corpus.py` | Turns `data/wikivoyage_raw/` into `data/japan_corpus.json`. Reproducible, no network needed. |
| `meridian.py` | Corpus loading, the evaluation set, and retrieval metrics. Helpers only; the components the chapter teaches live in notebook cells. |

## Data

| Path | Contents | Licence |
|---|---|---|
| `data/wikivoyage_raw/` | 78 raw Wikivoyage articles covering 12 Japanese cities, including the Kyoto and Tokyo district pages where most of the places live | CC BY-SA 4.0, Wikivoyage contributors |
| `data/japan_corpus.json` | Built artefact: 550 prose sections, 1,753 places, 1,105 with coordinates | as above |
| `data/meridian/` | A small travel knowledge base with planted failures (a superseded entry rule, an outdated fee, internal documents that must not reach a customer) plus a 20-question evaluation set | generated for the book |

## Code from the second edition

The CorpDocs pipeline (`rag.py`, `retriever.py`, `streamlit_app.py`) and the two
advanced-RAG notebooks are superseded by `03_retrieval.ipynb` and
`04_itinerary_assistant.ipynb`. They have not been removed from history: check
out the [`second_edition`](https://github.com/benman1/generative_ai_with_langchain/tree/second_edition)
branch if you want them. They target LangChain 0.3 and will not run on v1.
