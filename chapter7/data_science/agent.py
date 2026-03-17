"""Agent functionality."""
from typing import IO

import pandas as pd
from config import set_environment
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

from chapter7.data_science.prompts import PROMPT

set_environment()


def create_agent(csv: str | IO[bytes]) -> AgentExecutor:
    """
    Create data agent.

    Args:
        csv_file: The path to the CSV file.

    Returns:
        An agent executor.
    """
    llm = ChatOpenAI()
    df = pd.read_csv(csv)
    agent = create_pandas_dataframe_agent(
        llm, df, verbose=True, allow_dangerous_code=True, 
    )
    return agent

def query_agent(agent: AgentExecutor, query: str) -> str:
    """Query an agent and return the response."""
    prompt = PromptTemplate(template=PROMPT, input_variables=["query"])
    formatted_prompt = prompt.format(query=query)
    return agent.run(formatted_prompt)
