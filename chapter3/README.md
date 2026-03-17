# Chapter 3 - Building Workflows with LangGraph

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

| Section	| File | Colab	 | Kaggle	|
|-----------|--------|--------|-----------|
| Intro to LangGraph |  [notebook](langgraph_intro.ipynb)   | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/langgraph_intro.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Output parsers |  [notebook](output_parsers.ipynb)   | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/output_parsers.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Error handling | [notebook](error_handling.ipynb)  | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/error_handling.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Prompt templates | [notebook](prompt_templates.ipynb)     | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/prompt_templates.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Retry with error OutputParser | [notebook](retry_with_error_output_parser.ipynb)   | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/retry_with_error_output_parser.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Multimodality | [notebook](multimodality.ipynb)   | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/multimodality.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Map-reduce approach to handle long inputs |  [notebook](map_reduce.ipynb)  | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/map_reduce.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |
| Memory |  [notebook](memory.ipynb)  | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/memory.ipynb) | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/new) |

#### 📋 **Kaggle Import Instructions:**
To import any notebook to Kaggle:
1. Click the Kaggle badge above
2. Go to **File** → **Import Notebook** → **GitHub**
3. Paste the corresponding GitHub URL:
   - **LangGraph Intro**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/langgraph_intro.ipynb`
   - **Output Parsers**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/output_parsers.ipynb`
   - **Error Handling**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/error_handling.ipynb`
   - **Prompt Templates**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/prompt_templates.ipynb`
   - **Retry with Error OutputParser**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/retry_with_error_output_parser.ipynb`
   - **Multimodality**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/multimodality.ipynb`
   - **Map-Reduce**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/map_reduce.ipynb`
   - **Memory**: `https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/memory.ipynb`
