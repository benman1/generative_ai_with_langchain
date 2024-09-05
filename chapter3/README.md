# Chapter 3 - Getting Started with LangChain

Please make sure, you set up your environment with pip, conda, poetry, or docker!

You can set up the keys for the different providers with a `config.py` like this:
```python
import os

def set_environment():
    os.environ["OPENAI_API_KEY"] = "... "  # <- this has to be your api key!
    # I'm omitting all other keys
```

You can subsequently set all these keys for LangChain importing and executing the `set_environment()` function in your projects or notebooks:
```python
from config import set_environment
set_environment()
```


| Section	| File | Colab	 | Kaggle	| Gradient |
|-----------|--------|--------|-----------|----------|
| LLMs, prompts, and chat models |  [notebook](LLMs_chat_models_and_prompts.ipynb)   |        | | |
| Running local models |  [notebook](Running_local_models.ipynb)   |        | | |
| Customer service helper | [notebook](customer_service_use_case.ipynb)  |        | | |
| Using HuggingFace Hub models | [notebook](hf_hub_models.ipynb)     |        | | |
| Map-reduce for summarization | [notebook](map-reduce.ipynb)   |        | | |
| Tracking costs |  [notebook](tracking_costs.ipynb)  |        | | |


