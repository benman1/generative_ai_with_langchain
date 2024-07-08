"""Agent functionality."""
import pandas as pd
from config import set_environment
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI

from data_science.prompts import PROMPT

set_environment()


def create_agent(csv_file: str) -> AgentExecutor:
    """
    Create data agent.

    Args:
        csv_file: The path to the CSV file.

    Returns:
        An agent executor.
    """
    llm = OpenAI()
    df = pd.read_csv(csv_file)
    return create_pandas_dataframe_agent(llm, df, verbose=True)


def query_agent(agent: AgentExecutor, query: str) -> str:
    """Query an agent and return the response."""
    prompt = PromptTemplate(template=PROMPT, input_variables=["query"])
    return agent.run(prompt.format(query=query))
