# Generative AI with LangChain, First Edition
Build large language model (LLM) apps with Python, ChatGPT, and other LLMs!

This is the code repository for [Generative AI with LangChain, First Edition](https://www.packtpub.com/product/generative-ai-with-langchain/9781835083468), written by [Ben Auffarth](https://www.linkedin.com/in/ben-auffarth/?originalSubdomain=uk) and published by Packt. 

<a href="https://www.packtpub.com/product/generative-ai-with-langchain/9781835083468">
<img src="https://content.packt.com/B21269/cover_image_small.png" alt="Generative AI with LangChain - first edition" height="256px" align="right">
</a>

## Note to Readers
Thank you for choosing "Generative AI with LangChain"! We appreciate your enthusiasm and feedback.

<b>Code Updates: </b> 
Our commitment is to provide you with stable and valuable code examples. While LangChain is known for frequent updates, we understand the importance of aligning our code with the latest changes. The companion repository is regularly updated to harmonize with LangChain developments. </b>

<b>Expect Stability:</b>
For stability and usability, the repository might not match every minor LangChain update. We aim for consistency and reliability to ensure a seamless experience for our readers. 

<b>How to Reach Us:</b>
Encountering issues or have suggestions? Please don't hesitate to open an issue, and we'll promptly address it. Your feedback is invaluable, and we're here to support you in your journey with LangChain.

Thank you for your understanding and happy coding!

# Working with this repository
This is the companion repository for the book. Here are a few instructions that help getting set up. Please also see chapter 3. 

All chapters rely on Python. 

## Software and hardware list

| Chapter | Software required    | Link to the software    | Hardware specifications    | OS required    |
|:---:  |:---:  |:---:  |:---:  |:---:  |
| All chapters  | Python 3.10/3.11  | [https://www.python.org/downloads/](https://www.python.org/downloads/) | Should work on any recent computer | Windows, MacOS, Linux (any), macOS, Windows |

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

## Code validation
I've included a `Makefile` that includes instructions for validation with flake8, mypy, and other tools. I have run mypy like this:
```bash
make typecheck
```

To run the code validation in ruff, please run
```bash
ruff check .
```

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

1. What Is Generative AI
2. LangChain for LLM Apps
3. Getting Started with LangChain
4. Building Capable Assistants
5. Building a Chatbot like ChatGPT
6. Developing Software with Generative AI
7. LLMs for Data Science
8. Customizing LLMs and Their Output
9. Generative AI in Production
10. The Future of Generative Models,

### Chapter 01, What Is Generative AI

The chapter delves into the transformative impact of deep learning on processing and generating unstructured data, particularly focusing on large language models (LLMs). The widespread adoption of advanced AI models, driven by technological advancements and high-profile applications, has generated significant excitement in both the media and various industries. The chapter emphasizes the evolution of generative models and their applications, providing an overview of the technical concepts and training approaches that empower these models to produce novel content, primarily in the realms of text and image generation. While not delving into sound or video generation, the narrative aims to demystify the underlying mechanisms, including neural networks, large datasets, and computational scale, that enable these generative models to achieve human-like content generation. The structured exploration covers key topics, such as introducing generative AI, understanding LLMs, exploring text-to-image models, and examining AI applications in diverse domains.

**Key Insights**:
- **Evolution of Deep Learning:** Over the last decade, deep learning has undergone significant evolution, enabling the processing and generation of unstructured data, including text, images, and video.
- **Popularity of AI Models:** Advanced AI models, particularly large language models (LLMs), have gained widespread popularity across various industries, sparking excitement in the media and the business sector.
- **Transformative Impact of AI:** The chapter highlights the potential for a wide-ranging and major impact of Artificial Intelligence on businesses, societies, and individuals, driven by technological advancements and transformative possibilities in multiple sectors.
- **Generative Models Exploration:** The chapter explores generative models, providing a high-level understanding of technical concepts, training approaches, and the underlying magic that allows models to generate remarkably human-like content in text and image domains.

- **Comprehensive Overview:** From introducing generative AI and understanding LLMs to exploring text-to-image models and discussing AI applications in different domains, the chapter offers a structured and comprehensive overview of the evolving landscape of generative models.



### Chapter 02, LangChain for LLM Apps
The chapter introduces the limitations of Large Language Models (LLMs) like GPT-4 when used in isolation, emphasizing issues such as the lack of external knowledge, flawed reasoning, and the inability to take action. To address these challenges, the chapter proposes LangChain as a comprehensive framework that goes beyond mere API access to LLMs. It advocates for combining recent AI advancements with LangChain to build innovative language-based applications. The discussion begins by outlining the shortcomings faced when using LLMs independently and then introduces LangChain as a solution through integrations and off-the-shelf components. The chapter illustrates how developers can leverage LangChain's capabilities to create customized natural language processing solutions, emphasizing the importance of concepts like chains, action plan generation, and memory in understanding how LangChain works. By showcasing the potential of LangChain to overcome LLM limitations, the chapter sets the stage for exploring dynamic, data-aware applications that surpass the possibilities of simple API calls.

The chapter delves into the key components of LangChain, such as chains and agents, highlighting their role in composing pipelines and facilitating goal-oriented interactions. Chains enable sequencing calls to various resources, including LLMs, databases, and APIs, to accomplish multi-step workflows, while agents leverage these chains to take actions based on observations, managing dynamic applications. The concept of memory is introduced as well to persist information across executions, maintaining state and addressing the limitations of individual LLMs. The narrative emphasizes LangChain's reduction of complex orchestration into customizable building blocks, paving the way for the development of sophisticated applications. Looking ahead, the chapter teases the exploration of LangChain fundamentals in the subsequent chapters, promising the implementation of conversational agents that combine LLMs with knowledge bases and advanced reasoning algorithms. Developers are encouraged to unlock the full potential of LLMs by leveraging LangChain's capabilities to power the next generation of AI software.

**Key Insights**:
- **LLM Limitations Addressed:** The chapter highlights the limitations of Large Language Models (LLMs) like GPT-4, such as the lack of external knowledge and flawed reasoning, and introduces LangChain as a framework to overcome these challenges.

- **LangChain as a Solution:** LangChain is presented as a comprehensive solution to enhance LLM capabilities by combining them with other data sources and tools, offering developers the ability to build innovative language-based applications.

- **Components of LangChain:** The chapter explores key components of LangChain, including chains for sequencing calls to various resources, agents for goal-oriented interactions, and memory for persisting information across executions, providing modular and reusable building blocks.

- **Dynamic Applications:** LangChain enables the creation of dynamic, data-aware applications that go beyond the limitations of individual LLMs, illustrating the potential to reduce complex orchestration into customizable building blocks.

- **Next Steps with LangChain:** The chapter sets the stage for future exploration, teasing the implementation of conversational agents that combine LLMs with knowledge bases and advanced reasoning algorithms, showcasing how developers can unlock the full potential of LLMs to power the next generation of AI software.


### Chapter 03, Getting Started with LangChain
The chapter begins by providing essential setup instructions for the libraries required in the book, ensuring readers can execute the practical examples seamlessly using common dependency management tools like Docker, Conda, pip, and Poetry. Following this, the focus shifts to model integrations, introducing various models such as OpenAI's ChatGPT, Hugging Face models, and Jina AI. The chapter guides readers through the setup and interaction with these models, emphasizing the acquisition of API key tokens. As a practical application, the narrative culminates in the development of a real-world LLM app tailored for customer service, showcasing the potential game-changing impact of LLMs in this domain. This example serves to provide additional context for using LangChain, accompanied by tips and tricks for effective utilization.

**Key Insights**:
- **Comprehensive Environment Setup:** The chapter provides crucial setup instructions for required libraries using popular dependency management tools (Docker, Conda, pip, and Poetry), ensuring readers can smoothly run practical examples in the book.

- **Model Integrations Exploration:** It introduces and guides readers through various model integrations, including OpenAI's ChatGPT, Hugging Face models, and Jina AI. The focus is on acquiring API key tokens for these models, facilitating their usage in applications.

- **Real-world Application Development:** The chapter culminates in the development of a practical LLM app designed for customer service, showcasing the potential of LLMs to be game-changers in this domain. This example offers a tangible illustration of LangChain's capabilities.

- **LangChain Installation Methods:** Four distinct ways of installing LangChain and other necessary libraries are walked through, providing readers with multiple options to set up their environments effectively.

- **Orchestrating Multiple Models:** The chapter demonstrates LangChain's ability to orchestrate multiple models seamlessly, emphasizing its utility in reducing response times and ensuring accuracy in customer service interactions. The practical application involves text categorization and sentiment analysis.


### Chapter 04, Building Capable Assistants
The chapter focuses on addressing the challenge of transforming the fluency of Large Language Models (LLMs) into reliably capable assistants. It explores various methods to enhance LLMs through prompts, tools, and structured reasoning techniques, aiming to imbue greater intelligence, productivity, and trustworthiness. The chapter covers practical applications, beginning with mitigating hallucinations through automatic fact-checking, a critical step in improving the reliability of LLM outputs. The discussion then delves into the strength of LLMs in summarization, showcasing integration with prompts at different levels of sophistication and a map reduce approach for handling lengthy documents. The chapter further explores information extraction from documents through function calls, emphasizing the integration of external data and services to augment LLMs' limited world knowledge. The application of reasoning strategies is also demonstrated to extend the capabilities of LLMs. The integration of tools and function calling is explored beyond OpenAI, showcasing the evolution of instruction tuning and tool usage, enabling LLMs to automate tasks by interacting with real systems. The chapter illustrates the implementation of agents with LangChain, exemplified by a Streamlit app that answers research questions using external tools like search engines or Wikipedia. The incorporation of decision-making strategies, such as plan-and-solve and zero-shot agents, is also explored. 

**Key Insights**:
- **Enhancing LLM Reliability:** The chapter addresses the challenge of transforming the fluency of Large Language Models (LLMs) into reliable assistants by exploring methods such as prompts, tools, and structured reasoning techniques.

- **Fact-Checking for Accuracy:** The importance of mitigating hallucinations is highlighted through automatic fact-checking, offering practical approaches to verify claims against available evidence and reduce the spread of misinformation.

- **Summarization Techniques:** The chapter explores the strength of LLMs in summarization, demonstrating integration with prompts at different levels of sophistication and a map reduce approach for handling lengthy documents, providing practical applications for digesting extensive research articles or analyses.

- **Information Extraction and Tool Integration:** The integration of tools and function calling beyond OpenAI is showcased, illustrating how models can move beyond freeform text generation to automate tasks by interacting with real systems. The implementation of tools, such as a CV parser, demonstrates information extraction capabilities from documents.

- **Reasoning Strategies for Decision-Making:** The chapter introduces different strategies employed by agents for decision-making, including plan-and-solve and zero-shot agents in a Streamlit app. It emphasizes the importance of reasoning strategies to extend the capabilities of LLMs, paving the way for more capable and trustworthy AI assistants.


### Chapter 05, Building a Chatbot like ChatGPT
In this chapter, the focus is on addressing the limitations of chatbots powered by Large Language Models (LLMs), particularly their lack of world knowledge for domain-specific question answering. The solution explored is Retrieval-Augmented Generation (RAG), which improves chatbots by grounding their responses in external evidence sources. The key steps involve encoding corpora into vector embeddings for rapid semantic search, integrating retrieval results into the chatbot's prompt, and showcasing practical RAG implementations using popular libraries like Milvus and Pinecone. Through end-to-end examples, the chapter demonstrates how RAG significantly enhances chatbots' reasoning and factual correctness. The discussion extends to the reputational and legal perspective, emphasizing moderation capabilities in LangChain to check for harmful content in chatbot responses. The chapter provides a comprehensive exploration of chatbots, retrieval mechanisms, vector storage, memory mechanisms, and moderation, offering a foundational understanding and practical insights for implementing an advanced chatbot.

The chapter unfolds with an overview of chatbots, their evolution, and the current state of chatbot technology, highlighting practical implications and enhancements. It connects with the previous chapter on tool-augmented LLMs, emphasizing the importance of proactive communication and discussing retrieval mechanisms to improve chatbot accuracy. The exploration delves into loading documents, vector storage, and embedding, along with memory mechanisms for maintaining knowledge and ongoing conversation states. The chapter concludes with a discussion on moderation, underscoring the significance of ensuring respectful and aligned responses with organizational values. The features introduced in this chapter provide a starting point for investigating issues like memory, context, moderation of speech, and addressing challenges such as hallucinations in chatbot responses.

**Key Insights**:
- **Overcoming Knowledge Limitations:** The chapter addresses the limitations of chatbots powered by Large Language Models (LLMs) in domain-specific question answering by introducing Retrieval-Augmented Generation (RAG). RAG enhances chatbots by grounding responses in external evidence sources, overcoming the inherent lack of world knowledge in LLMs.

- **Vector-Based Retrieval:** The key techniques involve encoding corpora into vector embeddings, enabling rapid semantic search for relevant information. This vector-based retrieval approach is crucial for augmenting chatbot prompts with additional information retrieved from external sources.

- **Practical Implementations:** The chapter provides practical demonstrations of RAG implementations using popular libraries like Milvus and Pinecone, showcasing how these techniques significantly improve chatbots' reasoning and factual correctness. End-to-end examples offer insights into the integration of retrieval mechanisms into the chatbot's workflow.

- **Moderation Capabilities:** The importance of moderation is emphasized, highlighting LangChain's capability to pass text through a moderation chain for checking harmful content. This ensures that chatbot responses align with organizational values and adhere to ethical standards.

- **Foundational Understanding:** The chapter offers a foundational understanding of chatbots, retrieval mechanisms, vector storage, memory mechanisms, and moderation. It serves as a starting point for addressing challenges related to memory, context, and the moderation of speech in advanced chatbot implementations.

 
### Chapter 06, Developing Software with Generative AI
In this chapter, the focus shifts from integrating generative AI into software applications to leveraging Large Language Models (LLMs) for assistance in software development. The significance of generative AI in software development, highlighted by consultancies like KPMG and McKinsey, sets the stage for exploring the impact of LLMs in this domain. The chapter begins by providing a broad overview of the current state of using AI for software development, addressing how LLMs could enhance coding tasks and automate software development processes. Practical approaches are demonstrated by playing with different models, evaluating the generated code qualitatively, and implementing a fully automated agent for software development tasks using LangChain. The chapter emphasizes the potential extensions to this approach and provides insights into various practical approaches to automatic software development, all of which are accessible in the software_development directory in the GitHub repository for the book. While acknowledging the superficial correctness and potential bugs in suggested solutions, the chapter hints at the feasibility of LLMs learning to automate coding pipelines with the right architectural setup. It underscores the importance of human guidance on high-level design and rigorous review to prevent errors, suggesting that collaboration between humans and AI is likely the future path. 

**Key Insights**:
- **AI Impact on Software Development:** The chapter delves into the intersection of generative AI, particularly Large Language Models (LLMs), and software development, acknowledging reports from consultancies like KPMG and McKinsey highlighting AI's substantial impact on this domain.

- **Coding Assistance with LLMs:** LLMs are explored as valuable coding assistants in software development, with a focus on automating coding tasks. The chapter qualitatively evaluates code generation using various models, showcasing their potential benefits and limitations.

- **Automated Software Development Agent:** Practical implementations are demonstrated through the creation of a fully automated agent for software development tasks using LangChain. The chapter discusses design choices and presents results, emphasizing the extensibility of this approach.

- **Feasibility of Automating Coding Pipelines:** The chapter raises the possibility that, with the right architectural setup, LLMs could learn to automate coding pipelines. It acknowledges current limitations and suggests that human guidance and collaboration between humans and AI are crucial for safety and reliability.

- **Future Directions and Collaborative Development:** While highlighting the potential for automating coding tasks, the chapter acknowledges the need for high-level design guidance and rigorous human review to prevent errors. It suggests the future likely involves collaboration between humans and AI in the realm of software development.


### Chapter 07, LLMs for Data Science
This chapter explores the role of generative AI, particularly Large Language Models (LLMs), in automating data science processes. It highlights the potential of LLMs to accelerate scientific progress, especially in the efficient analysis of research data and literature review processes. The chapter begins with an examination of the impact of generative models on data science, emphasizing how LLMs contribute to the automation of various stages in the data science pipeline. The discussion covers automated data science, the use of code generation and tools to answer data science questions, and the exploration of structured datasets through LLM-powered processes. Practical approaches to data science with LLMs are demonstrated throughout the chapter, providing insights that can be explored further in the data_science directory in the GitHub repository for the book.

**Key Insights**:
- **Generative AI Impact on Data Science:** The chapter explores the profound impact of generative AI, particularly Large Language Models (LLMs), on data science. It highlights how LLMs can accelerate scientific progress by efficiently analyzing research data and aiding in literature review processes.

- **Automated Data Science Pipeline:** The discussion revolves around the automation of the data science pipeline, showcasing the value of Automated Machine Learning (AutoML) frameworks and the integration of LLMs in various stages, from data preparation to model deployment.

- **Code Generation and Tool Utilization:** The chapter demonstrates the diverse applications of LLMs in data science, including code generation and tool utilization to answer questions and enhance datasets. It draws parallels with software development and explores the augmentation of datasets through external tools like WolframAlpha.

- **LLMs for Data Exploration:** Practical approaches to data exploration with LLMs are presented, focusing on the analysis of structured datasets. The exploration involves the effective use of LLM-powered processes for ingesting and analyzing textual data, extending the techniques introduced in previous chapters.

- **Augmentation, Not Replacement:** While acknowledging the transformative potential of AI technologies in data analysis, the chapter emphasizes that the current state of AI technology augments rather than replaces human expertise in data science. It broadens the analytical toolset for professionals, showcasing the collaborative potential of human-AI interaction. The next chapter is teased to focus on conditioning techniques to enhance LLM performance through prompting and fine-tuning.


### Chapter 08, Customizing LLMs and Their Output
This chapter focuses on enhancing the reliability and performance of Large Language Models (LLMs) in specific scenarios, particularly complex reasoning and problem-solving tasks, through the process of conditioning. Conditioning, crucial for steering generative AI, is achieved through two main techniques: fine-tuning and prompting. Fine-tuning involves training the pre-trained base model on specific tasks or datasets relevant to the desired application, allowing the model to adapt and become more accurate and contextually relevant. Prompt engineering, on the other hand, involves providing additional input or context at inference time to generate text tailored to a particular task or style. The chapter delves into advanced prompt engineering strategies such as few-shot learning, tree-of-thought, and self-consistency, demonstrating their implementation throughout the chapter with corresponding code available in the GitHub repository for the book. The chapter serves as a practical guide for researchers and practitioners working with LLMs to unlock advanced conditioning strategies and sets the stage for the next chapter on the productionization of generative AI.

**Key Insights**:
- **Conditioning for Performance Improvement:** The chapter focuses on the critical concept of conditioning in generative AI, highlighting its role in steering LLMs to enhance reliability, safety, and overall performance in complex reasoning and problem-solving scenarios.

- **Fine-Tuning for Adaptation:** Fine-tuning emerges as a key technique for conditioning LLMs, involving training the pre-trained base model on specific tasks or datasets relevant to the desired application. This process allows the model to adapt and achieve greater accuracy and contextual relevance for the intended use case.

- **Significance of Prompt Engineering:** The chapter underscores the importance of prompt engineering as a means to unlock LLM reasoning capabilities. By providing additional input or context at inference time, prompt engineering enables LLMs to generate text tailored to specific tasks or styles, with advanced strategies such as few-shot learning and self-consistency explored.

- **Diverse Prompting Techniques:** Various prompting techniques are discussed, including step-by-step prompting, alternate selection, inference prompts, problem decomposition, and sampling multiple responses. These methods contribute to improving the reliability of LLMs in complex reasoning tasks, enhancing accuracy and consistency.

- **Application of Advanced Conditioning Strategies:** Throughout the chapter, practical implementations of advanced conditioning strategies, such as fine-tuning and prompt engineering, are demonstrated. The code corresponding to these implementations can be found in the GitHub repository for the book, providing a valuable resource for researchers and practitioners working with LLMs.


### Chapter 09, Generative AI in Production
This chapter focuses on the practical considerations and best practices for deploying generative AI, specifically Large Language Model (LLM) apps, from research to real-world applications. The transition from controlled research settings to live production environments involves addressing challenges related to performance, scalability, regulatory compliance, and ethical considerations. The chapter covers key aspects such as getting LLM apps ready for production, evaluating their performance, deploying them effectively, and observing their behavior in live environments. The importance of offline evaluation and continuous observability is emphasized to ensure a model's abilities are understood in a controlled setting and monitored in real-time production environments.

Throughout the chapter, practical examples with LLM apps are provided, offering insights into techniques for fine-tuning, safety interventions, and defensive design to develop applications that produce reliable and meaningful outputs. The discussion extends to deployment tools like FastAPI, Ray, and LangServe, with a focus on the significance of evaluation metrics, comparative evaluation, and systematic monitoring in ensuring the quality, accuracy, and reliability of LLMs in production

**Key Insights**:
- **Deployment Challenges and Considerations:** The chapter addresses the complex challenges of deploying generative AI, particularly Large Language Model (LLM) apps, in real-world production scenarios. It emphasizes the need for scalability, monitoring, and ethical safeguards to navigate the transition from research to live environments effectively.

- **Critical Evaluation Processes:** The importance of both offline evaluation and continuous observability is highlighted. These processes provide essential insights into a model's performance, quality, and behavior, ensuring that LLMs produce reliable, useful, and sensible outputs. LangChain supports comparative evaluation, criteria checking, and semantic similarity metrics for a comprehensive evaluation strategy.

- **Deployment Tools and Techniques:** Practical examples in the chapter involve deploying applications with tools like FastAPI, Ray, and LangServe. The discussion extends to the role of LangSmith, which provides powerful capabilities for tracking, benchmarking, and optimizing LLMs built with LangChain. The emphasis is on the evolving landscape of deployment tools and the significance of staying informed about emerging developments.

- **Monitoring for Performance and Reliability:** Monitoring LLMs is identified as a vital aspect of deployment and maintenance. The chapter introduces key metrics for a comprehensive monitoring strategy and offers examples of how to track these metrics in practice. Tools such as PromptWatch and LangSmith are discussed to enhance observability, accelerate development, and validate LLMs.

- **Responsibility in Generative AI:** The chapter underscores the importance of responsible deployment, emphasizing meticulous planning around scalability, interpretability, testing, and monitoring. Techniques like fine-tuning, safety interventions, and defensive design are crucial for developing applications that produce helpful, harmless, and readable outputs. The responsible deployment of generative AI models holds immense potential benefits across industries, from medicine to education.

### Chapter 10, The Future of Generative Models
The chapter begins with an exploration of the current state of generative AI models, acknowledging recent breakthroughs while highlighting persisting challenges related to precision, reasoning, controllability, and biases within these models. It emphasizes the technical and practical aspects, such as the black-box nature of models, limited interpretability, and concerns regarding biases in training data. The discussion anticipates sophisticated capabilities in the coming decades but underscores the need for addressing challenges to ensure responsible and controllable AI development.

The focus then shifts to the economic consequences and societal implications of generative AI. The text discusses the surge in venture funding for generative AI start-ups and major investments by industry leaders, indicating the technology's potential economic impact. The chapter also touches on societal concerns, including misinformation, plagiarism, deepfake proliferation, and the possible weaponization of generative AI, urging a thoughtful approach to regulations and practical implementation to address these challenges responsibly.

**Key Insights**:
- **Current State of Generative AI Models:** Explore the current state of generative AI models, emphasizing recent breakthroughs, persistent challenges, and technical considerations such as interpretability and biases.

- **Economic Impact and Venture Funding:** Discuss the economic consequences of generative AI, highlighting the surge in venture funding for start-ups and significant investments by major players like Salesforce and Accenture.

- **Job Displacement and Democratization of Skills:** Address concerns about job losses, particularly in specialized roles, and examine the potential democratization of skills enabled by generative AI.

- **Societal Implications and Ethical Considerations:** Delve into the societal implications, including issues related to misinformation, plagiarism, deepfakes, and the potential weaponization of generative AI. Discuss ethical considerations and the need for responsible regulations.

- **Future Challenges and Collaborative Governance:** Anticipate future challenges in the ethical and technical domains, emphasizing the importance of proactive governance, collaboration between stakeholders, and alignment with human values in directing generative AI technologies toward benevolent outcomes.


> If you feel this book is for you, get your [copy](https://www.amazon.com/Generative-AI-LangChain-language-ChatGPT/dp/1835083463/ref=sr_1_2?crid=2XYQSRSV1SUSF&keywords=Langchain&qid=1703044611&sprefix=langchain%2Caps%2C552&sr=8-2) today! <img alt="Coding" height="15" width="35"  src="https://media.tenor.com/ex_HDD_k5P8AAAAi/habbo-habbohotel.gif">

## Know more on the Discord server <img alt="Coding" height="25" width="32"  src="https://cliply.co/wp-content/uploads/2021/08/372108630_DISCORD_LOGO_400.gif">
You can get more engaged on the discord server for more latest updates and discussions in the community at [Discord](https://packt.link/lang)

## Download a free PDF <img alt="Coding" height="25" width="40" src="https://emergency.com.au/wp-content/uploads/2021/03/free.gif">

_If you have already purchased a print or Kindle version of this book, you can get a DRM-free PDF version at no cost. Simply click on the link to claim your free PDF._
[Free-Ebook](https://packt.link/free-ebook/9781835083468) <img alt="Coding" height="15" width="35"  src="https://media.tenor.com/ex_HDD_k5P8AAAAi/habbo-habbohotel.gif">

We also provide a PDF file that has color images of the screenshots/diagrams used in this book at [GraphicBundle](https://packt.link/gbp/9781835083468) <img alt="Coding" height="15" width="35"  src="https://media.tenor.com/ex_HDD_k5P8AAAAi/habbo-habbohotel.gif">


## Get to know the Author
_Ben Auffarth_ A seasoned data science leader with a background and Ph.D. in computational neuroscience. Ben has analyzed terabytes of data, simulated brain activity on supercomputers with up to 64k cores, designed and conducted wet lab experiments, built production systems processing underwriting applications, and trained neural networks on millions of documents. He’s the author of the books Machine Learning for Time Series and Artificial Intelligence with Python
Cookbook. He now works in insurance at Hastings Direct.

## Other Related Books
- [Transformers for Natural Language Processing and Computer Vision](https://www.packtpub.com/product/transformers-for-natural-language-processing-and-computer-vision-third-edition/9781805128724)
- [Building LLM Apps](https://www.packtpub.com/product/building-llm-apps/9781835462317)
- [Generative AI Engineering](https://www.packtpub.com/product/generative-ai-engineering-1e/9781805120513)
