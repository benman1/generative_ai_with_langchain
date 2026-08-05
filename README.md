<h1 align="center">
Generative AI with LangChain and LangGraph, Third Edition</h1>
<p align="center">This is the code repository for <b>Generative AI with LangChain and LangGraph, Third Edition</b>, to be published by Packt.
</p>

<h2 align="center">
Build production-ready LLM applications and advanced agents with Python, LangChain v1 and LangGraph
</h2>
<p align="center">
Ben Auffarth, Leonid Kuligin</p>

<p align="center">
   <a href="https://discord.gg/YQbX5rsc74" alt="Discord" title="Learn more on the Discord server"><img width="32px" src="https://cliply.co/wp-content/uploads/2021/08/372108630_DISCORD_LOGO_400.gif"/></a>
</p>
<details open> 
  <summary><h2>About the book</summary>
The third edition is rebuilt around <b>LangChain v1</b> and <b>LangGraph v1</b>, the first releases where the agent and graph APIs settled into a stable shape. It covers what it takes to move an LLM prototype into production: graph-based workflows you can inspect and resume, agents with explicit tool boundaries, retrieval that is measured rather than assumed, and the evaluation and observability layers that tell you whether any of it works.

RAG coverage is expanded well past hybrid search and re-ranking into a failure taxonomy you can debug against, and a full human-in-the-loop project. Chapters on testing, evaluation and deployment address what changes when real users arrive, and every chapter ships runnable notebooks that work without a paid API key wherever that is possible.

</details>
<details open> 
  <summary><h2>Key Learnings</summary>

<ul>
<li>Design and implement refined multi-agent systems using LangGraph</li>
<li>Enterprise-grade testing and evaluation frameworks for LLM applications</li>
<li>Deploy production-ready observability and monitoring solutions</li>
<li>Build RAG systems with hybrid search and re-ranking capabilities</li>
<li>Implement agents for software development and data analysis</li>
<li>Work with latest LLMs and providers Google Gemini, Anthropic and Mistral, DeepSeek, and OpenAI o3-mini</li>
<li>Optimize cost and performance across different deployment types</li>
<li>Design secure, compliant AI systems with current best practices</li>
</ul>

  </details>
  <details open>
<summary><h2>Note to Readers</summary>

Thank you for choosing "Generative AI with LangChain and LangGraph"! We appreciate your enthusiasm and feedback.

The book has been through several editions, and each has its own branch:
* [third_edition](https://github.com/benman1/generative_ai_with_langchain/tree/third_edition) - **this branch**, for the 3rd edition, targeting **LangChain v1.0 and above** and LangGraph v1.
* [second_edition](https://github.com/benman1/generative_ai_with_langchain/tree/second_edition) - the 2nd edition, corresponding to LangChain 0.3.
* [softupdate](https://github.com/benman1/generative_ai_with_langchain/tree/softupdate) - the soft update of the book (2024), corresponding to LangChain 0.1.13.
* [main](https://github.com/benman1/generative_ai_with_langchain/tree/main) - the original version of the book (December 2023).

**LangChain v1 is a breaking change.** `langchain.retrievers` and `langchain.chains` no longer exist; compression retrievers, rerankers and the legacy chains moved to the separate `langchain-classic` package, which `pip install langchain` does not pull in. `langchain-community` is archived and `langchain-experimental` is being sunset: both still import, both warn. Code from the 2nd edition branch will not run unchanged.

Please refer to the version that you are interested in or that corresponds to your version of the book.
</details>


<details open>
<summary><h3>Commitment</summary>

<b>Code Updates:</b> Our commitment is to provide you with stable and valuable code examples. While LangChain is known for frequent updates, we understand the importance of aligning our code with the latest changes. The companion repository is regularly updated to harmonize with LangChain developments.

<b>Expect Stability:</b> For stability and usability, the repository might not match every minor LangChain update. We aim for consistency and reliability to ensure a seamless experience for our readers. 

<b>How to Reach Us:</b> Encountering issues or have suggestions? Please don't hesitate to open an issue, and we'll promptly address it. Your feedback is invaluable, and we're here to support you in your journey with LangChain.
Thank you for your understanding and happy coding!
</details>

<details open> 
   <summary><h3>Know more on the Discord server <img alt="Coding" height="25" width="32"  src="https://cliply.co/wp-content/uploads/2021/08/372108630_DISCORD_LOGO_400.gif"></summary>

You can engage with the author and other readers on the discord server and find latest updates and discussions in the community at [Discord](https://discord.gg/YQbX5rsc74)
</details>

<details open> 
  <summary><h2>Chapters</summary>

In the following table, you can find links to the directories in this repository. Each directory contains further links to python scripts and to notebooks. You can also see links to computing platforms, where you can execute the notebooks in the repository. Please note that there are other Python scripts and projects that are not notebooks, which you'll find in the chapter directories.

| Chapter | Title | Directory Link |
|---------|-------|----------------|
| Chapter 1 | The Rise of Generative AI: From Language Models to Agents | [chapter1/](./chapter1) |
| Chapter 2 | First Steps with LangChain | [chapter2/](./chapter2) |
| Chapter 3 | Building Workflows with LangGraph | [chapter3/](./chapter3) |
| Chapter 4 | Retrieval Augmented Generation | [chapter4/](./chapter4) |
| Chapter 5 | Building Intelligent Agents | [chapter5/](./chapter5) |
| Chapter 6 | Advanced Applications and Multi-Agent Systems | [chapter6/](./chapter6) |
| Chapter 7 | Software Development and Data Analysis Agents | [chapter7/](./chapter7) |
| Chapter 8 | Evaluation and Testing of LLM Applications | [chapter8/](./chapter8) |
| Chapter 9 | Production Deployment and Observability | [chapter9/](./chapter9) |

</details>


<details open> 
  <summary><h2>Requirements for this book</summary>
  
### Software and hardware list
This is the companion repository for the book. Here are a few instructions that help getting set up. Please also see chapter 2. 

All chapters rely on Python. 

Please check the instructions for setting up the environment either in the book or [here](./SETUP.md). They include instructions for dependencies and API keys. **Following the instructions should make sure that you don't have any issues running the code in the book or this repository. If you encounter any issues, please make sure you've followed these instructions.**


## 👋 Contribute

We welcome contributions from developers of all levels. If you'd like to contribute, please check our [contributing guidelines](./CONTRIBUTING.md) and help make this repository and the book more accessible.

---
[![Star History Chart](https://api.star-history.com/svg?repos=benman1/generative_ai_with_langchain&type=Timeline)](https://star-history.com/#benman1/generative_ai_with_langchain&Date)


## ❤️ Contributors

[![repo contributors](https://contrib.rocks/image?repo=benman1/generative_ai_with_langchain)](https://github.com/benman1/generative_ai_with_langchain/graphs/contributors)


<details> 
  <summary><h2>Get to know Authors</h2></summary>

_Ben Auffarth_ Ben Auffarth is a full-stack data scientist with more than 15 years of work experience. With a background and Ph.D. in computational and cognitive neuroscience, he has designed and conducted wet lab experiments on cell cultures, analyzed experiments with terabytes of data, run brain models on IBM supercomputers with up to 64k cores, built production systems processing hundreds and thousands of transactions per day, and trained language models on a large corpus of text documents. He co-founded and is the former president of Data Science Speakers, London.

_Leonid Kuligin_ Leonid Kuligin is a staff AI engineer at Google Cloud, working on generative AI and classical machine learning solutions (such as demand forecasting or optimization problems). Leonid is one of the key maintainers of Google Cloud integrations on LangChain, and a visiting lecturer at CDTM (TUM and LMU). Prior to Google, Leonid gained more than 20 years of experience in building B2C and B2B applications based on complex machine learning and data processing solutions such as search, maps, and investment management in German, Russian, and US technological, financial, and retail companies.



</details>
