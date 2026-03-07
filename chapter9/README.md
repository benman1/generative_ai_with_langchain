# Chapter 9 - Production Deployment and Observability

This directory contains code examples for deploying and monitoring LLM applications in production environments.

| Section | File | Description | Colab | Kaggle |
|---------|------|-------------|-------|--------|
| Web Service | [main.py](fastapi/main.py) | Implements a production-ready web server with FastAPI that handles both standard HTTP requests and WebSocket connections for streaming LLM responses | x | x |
| Distributed Computing | [build_index.py](ray/build_index.py) | Demonstrates how to build a FAISS vector index from documentation using Ray for distributed processing | x | x |
| API Serving | [serve_index.py](ray/serve_index.py) | Shows how to serve a pre-built FAISS index as an API endpoint using Ray Serve with robust error handling | x | x |
| Observability | [prompt_tracking.py](prompt_tracking.py) | Integrates PromptWatch for monitoring and tracking LLM prompts and responses in production | x | x |
| Chat Interface | [chat.py](chat.py) | Implements a simple chat interface for interacting with LLM models | x | x |
| Vector Stores | [indexing.py](indexing.py) | Demonstrates how to create and manage vector store indexes for retrieval-augmented generation | x | x |
| Search API | [serve_vector_store.py](serve_vector_store.py) | Shows how to serve a vector store as an API for semantic search capabilities | x | x |
| Agent Monitoring | [tracing.py](tracing.py) | Implements tracing and trajectory tracking for LLM agents to monitor execution paths | x | x |

## Requirements

Please make sure you set up your environment with pip, conda, poetry, or docker! You can set up the keys for the different providers in a `config.py` as recommended in the book. Please check the [setup instructions](../SETUP.md) for dependencies and API keys before you start.

## Usage

Each notebook can be run as a standalone example. For detailed instructions, see the comments within each file.

### FastAPI Deployment

The FastAPI example demonstrates how to create a web service with both standard REST endpoints and WebSocket support for streaming responses. To run (from root):

```bash
PYTHONPATH=. python chapter9/fastapi/main.py
```

Then visit http://localhost:8000 in your browser.

### Ray Serve Deployment

The Ray examples show how to build and serve a searchable index using distributed computing:

```bash
cd ray
# First build the index
python build_index.py
# Then serve it
python serve_index.py
```

Access the API at http://localhost:8000/?query=your+search+query

### Observability Tools

The observability examples demonstrate how to implement monitoring for LLM applications:

```bash
# For prompt tracking
python prompt_tracking.py

# For agent tracing
python tracing.py
```


