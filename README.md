# Generative AI with LangChain, First Edition
Build large language model (LLM) apps with Python, ChatGPT, and other LLMs!

This is the code repository for [Generative AI with LangChain, First Edition](https://www.packtpub.com/product/generative-ai-with-langchain/9781835083468), written by [Ben Auffarth](https://www.linkedin.com/in/ben-auffarth/?originalSubdomain=uk) and published by Packt. 

<a href="https://www.packtpub.com/product/generative-ai-with-langchain/9781835083468">
<img src="https://content.packt.com/B21269/cover_image_small.png" alt="Generative AI with LangChain - first edition" height="256px" align="right">
</a>

## Note to Readers
Thank you for choosing "Generative AI with LangChain"! We appreciate your enthusiasm and feedback.

**Please note that we've released an update of the book that includes significant updates.** These is be available for anyone who has bought the book before the new release as an electronic copy. Consequently, there are two different branches for this repository: 
* [main](https://github.com/benman1/generative_ai_with_langchain/tree/main) - this is the original version of the book.
* [softupdate](https://github.com/benman1/generative_ai_with_langchain/tree/softupdate) - this is for the latest update of the book, corresponding to version 0.1.13 of LangChain.

Please refer to the version that you are interested in or that corresponds to your version of the book.

### Download a free PDF <img alt="Coding" height="25" width="40" src="https://emergency.com.au/wp-content/uploads/2021/03/free.gif">

_If you have already purchased an up-to-date print or Kindle version of this book, you can get a DRM-free PDF version at no cost. Simply click on the link to claim your free PDF._
[Free-Ebook](https://packt.link/free-ebook/9781835083468) <img alt="Coding" height="15" width="35"  src="https://media.tenor.com/ex_HDD_k5P8AAAAi/habbo-habbohotel.gif">

We also provide a PDF file that has color images of the screenshots/diagrams used in this book at [GraphicBundle](https://packt.link/gbp/9781835083468) <img alt="Coding" height="15" width="35"  src="https://media.tenor.com/ex_HDD_k5P8AAAAi/habbo-habbohotel.gif">

### Commitment
<b>Code Updates: </b> 
Our commitment is to provide you with stable and valuable code examples. While LangChain is known for frequent updates, we understand the importance of aligning our code with the latest changes. The companion repository is regularly updated to harmonize with LangChain developments. </b>

<b>Expect Stability:</b>
For stability and usability, the repository might not match every minor LangChain update. We aim for consistency and reliability to ensure a seamless experience for our readers. 

<b>How to Reach Us:</b>
Encountering issues or have suggestions? Please don't hesitate to open an issue, and we'll promptly address it. Your feedback is invaluable, and we're here to support you in your journey with LangChain.
Thank you for your understanding and happy coding!

#### Know more on the Discord server <img alt="Coding" height="25" width="32"  src="https://cliply.co/wp-content/uploads/2021/08/372108630_DISCORD_LOGO_400.gif">
You can get more engaged on the discord server for more latest updates and discussions in the community at [Discord](https://packt.link/lang)

## Software and hardware list
This is the companion repository for the book. Here are a few instructions that help getting set up. Please also see chapter 3. 

All chapters rely on Python. 

| Chapter | Software required    | Link to the software    | Hardware specifications    | OS required    |
|:---:  |:---:  |:---:  |:---:  |:---:  |
| All chapters  | Python 3.11  | [https://www.python.org/downloads/](https://www.python.org/downloads/) | Should work on any recent computer | Windows, MacOS, Linux (any), macOS, Windows |

Please note that Python 3.12 might not work (see [#11](/../../issues/11)).

## Environment
You can install your local environment with conda (recommended) or pip. The environment configurations for conda and pip are provided. Please note that if you choose pip as you installation tool, you might need additional tweaking.

If you have any problems with the environment, please raise an issue, where you show the error you got. If you feel confident, please go ahead and create a pull request.

For pip and poetry, make sure you install pandoc in your system. On MacOS use brew:
```bash
brew install pandoc
```

On Ubuntu or Debian linux, use apt:
```bash
sudo apt-get install pandoc
```

On Windows, you can use an [installer](https://github.com/jgm/pandoc/releases/latest).

### Conda
This is the recommended method for installing dependencies. Please make sure you have [anaconda](https://www.anaconda.com/download) installed.

First create the environment for the book that contains all the dependencies:
```bash
conda env create --file langchain_ai.yaml --force
```

The conda environment is called `langchain_ai`. You can activate it as follows:
```bash
conda activate langchain_ai 
```

### Pip
[Pip](https://pypi.org/project/pip/) is the default dependency management tool in Python. With pip, you should be able to install all the libraries from the requirements file:

```bash
pip install -r requirements.txt
```

If you are working with a slow internet connection, you might see a timeout with pip (this can also happen with conda and pip). As a workaround, you can increase the timeout setting like this:
```bash
export PIP_DEFAULT_TIMEOUT=100
```

### Docker
There's a [docker](https://www.docker.com/) file for the environment as well. It uses the docker environment and starts an ipython notebook. To use it, first build it, and then run it:

```bash
docker build -t langchain_ai .
docker run -d -p 8888:8888 langchain_ai
```

You should be able to find the notebook in your browser at [http://localhost:8888](http://localhost:8888).

### Poetry

Make sure you have [poetry](https://python-poetry.org/) installed. On Linux and MacOS, you should be able to use the requirements file:
```bash
poetry install --no-root
```
This should take the `pyproject.toml` file and install all dependencies.

## Setting API keys
Following best practices regarding safety, I am not committing my credentials to GitHub. You might see `import` statements  mentioning a `config.py` file, which is not included in the repository. This module has a method `set_environment()` that sets all the keys as environment variables like this:

Example config.py:

```python
import os

def set_environment():
     os.environ['OPENAI_API_KEY']='your-api-key-here'
```

Obviously, you'd put your API credentials here. Depending on the integration (Openai, Azure, etc) you need to add the corresponding API keys. The OpenAI API keys are the most often used across all the code. 

You can find more details about API credentials and setup in chapter 3 of the book [Generative AI with LangChain](https://www.amazon.com/Generative-AI-LangChain-language-ChatGPT-ebook/dp/B0CBBL55PQ).


## Contributing

If you find anything amiss with the notebooks or dependencies, please feel free to create a pull request.

If you want to change the conda dependency specification (the yaml file), you can test it like this:
```bash
conda env create --file langchain_ai.yaml --force
```

You can update the pip requirements like this:
```bash
pip freeze > requirements.txt
```

Please make sure that you keep these two ways of maintaining dependencies in sync.

Then make sure, you test the notebooks in the new environment to see that they run.

### Code validation
I've included a `Makefile` that includes instructions for validation with flake8, mypy, and other tools. I have run mypy like this:
```bash
make typecheck
```

To run the code validation in ruff, please run
```bash
ruff check .
```

# Generative AI with LangChain 
Create generative AI apps with LangChain.

## About the book

ChatGPT and the GPT models by OpenAI have brought about a revolution not only in how we write and research but also in how we can process information. This book discusses the functioning, capabilities, and limitations of LLMs underlying chat systems, including ChatGPT and Bard. It also demonstrates, in a series of practical examples, how to use the LangChain framework to build production-ready and responsive LLM applications for tasks ranging from customer support to software development assistance and data analysis – illustrating the expansive utility of LLMs in real-world applications.

Unlock the full potential of LLMs within your projects as you navigate through guidance on fine-tuning, prompt engineering, and best practices for deployment and monitoring in production environments. Whether you're building creative writing tools, developing sophisticated chatbots, or crafting cutting-edge software development aids, this book will be your roadmap to mastering the transformative power of generative AI with confidence and creativity.


## Key Takeaways
- Understand LLMs, their strengths and limitations
- Grasp generative AI fundamentals and industry trends
- Create LLM apps with LangChain like question-answering systems and chatbots
- Understand transformer models and attention mechanisms
- Automate data analysis and visualization using pandas and Python
- Grasp prompt engineering to improve performance
- Fine-tune LLMs and get to know the tools to unleash their power
- Deploy LLMs as a service with LangChain and apply evaluation strategies
- Privately interact with documents using open-source LLMs to prevent data leaks

## Outline and Chapter Summary

This book is a comprehensive introduction to LLMs and LangChain, demystifying the basic mechanics of LangChain, its functionalities, and the myriad of applications it can be integrated into.

> If you feel this book is for you, get your [copy](https://amzn.to/3IZevQC) today! <img alt="Coding" height="15" width="35"  src="https://media.tenor.com/ex_HDD_k5P8AAAAi/habbo-habbohotel.gif">

## Get to know the Author
_Ben Auffarth_ A seasoned data science leader with a background and Ph.D. in computational neuroscience. Ben has analyzed terabytes of data, simulated brain activity on supercomputers with up to 64k cores, designed and conducted wet lab experiments, built production systems processing underwriting applications, and trained neural networks on millions of documents. He’s the author of the books Machine Learning for Time Series and Artificial Intelligence with Python
Cookbook. He now works in insurance at Hastings Direct.

