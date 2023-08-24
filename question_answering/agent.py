"""Create an agent executor to use in the research app.

TODO: make sure history is maintained and used in conversation!
"""
from typing import Literal

from langchain import LLMChain, PromptTemplate
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner


ReasoningStrategies = Literal["one-shot-react", "plan-and-solve"]

from config import set_environment

set_environment()


def load_agent(
        tool_names: list[str],
        strategy: ReasoningStrategies = "one-shot-react"
) -> Chain:
    """Logic to build up an agent.

    Please note the absence of any memory here. This can be
    easily improved by adding a conversational memory.

    By default, should use tools like these:
    * DuckDuckGoSearchRun, wolfram alpha, arxiv search, wikipedia

    plan_and_execute means that all plans are made ahead of time
    (as opposed to one-shot-react).

    For a private chatbot try GPT4All, for example:
    llm = GPT4All(model="/Users/ben/Downloads/orca-mini-3b.ggmlv3.q4_0.bin")
    """
    llm = ChatOpenAI(temperature=0, streaming=True)
    if len(tool_names) == 0:
        # if there are no tools, no point building a tool agent
        return LLMChain(llm=llm, prompt=PromptTemplate(
            template="Try to answer this question: {question}. "
                     "If you don't know the answer, say you don't know.",
            input_variables=["question"]
        ))

    tools = load_tools(
        tool_names=tool_names,
        llm=llm
    )
    if strategy == "plan-and-solve":
        planner = load_chat_planner(llm)
        executor = load_agent_executor(llm, tools, verbose=True)
        return PlanAndExecute(planner=planner, executor=executor, verbose=True)

    # Occasionally, we might come across a output parsing error.
    # We can handle these by setting "handle_parsing_errors"
    return initialize_agent(
        tools=tools, llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors="Check your output and make sure it conforms!"
    )
