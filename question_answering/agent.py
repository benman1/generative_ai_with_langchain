from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI


def load_agent(tool_names: list[str], self_check: bool = False) -> Chain:
    """Logic to build up an agent.

    By default should use tools like these:
    * DuckDuckGoSearchRun, wolfram alpha, arxiv search, wikipedia

    For a private chatbot try GPT4All, for example:
    llm = GPT4All(model="/Users/ben/Downloads/orca-mini-3b.ggmlv3.q4_0.bin")
    """
    llm = ChatOpenAI(temperature=0, streaming=True)
    tools = load_tools(
        tool_names=tool_names,
        llm=llm
    )
    return initialize_agent(
        tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
