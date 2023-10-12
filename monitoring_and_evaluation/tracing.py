"""Tracing of agent calls and intermediate results."""
import subprocess

from langchain.agents.openai_functions_agent.base import _FunctionsAgentAction
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage
from langchain.tools import tool
from langchain.agents import AgentType, initialize_agent

from pydantic import HttpUrl
from urllib.parse import urlparse
from config import set_environment

set_environment()

@tool
def ping(url: HttpUrl, return_error: bool) -> str:
    """Ping the fully specified url. Must include https:// in the url."""
    hostname = urlparse(str(url)).netloc
    completed_process = subprocess.run(
        ["ping", "-c", "1", hostname], capture_output=True, text=True
    )
    output = completed_process.stdout
    if return_error and completed_process.returncode != 0:
        return completed_process.stderr
    return output


llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)
agent = initialize_agent(
    llm=llm,
    tools=[ping],
    agent=AgentType.OPENAI_MULTI_FUNCTIONS,
    return_intermediate_steps=True,  # IMPORTANT!
)

result = agent("What's the latency like for https://langchain.com?")
print(result)

if __name__ == "__main__":
    pass
