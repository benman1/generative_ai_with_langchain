"""Tracing of agent calls and intermediate results."""
import subprocess
from urllib.parse import urlparse

from config import set_environment
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import HttpUrl

set_environment()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a network assistant. Use tools to check latency."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

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


tools = [ping]
llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, return_intermediate_steps=True
)

result = agent_executor.invoke(
    {"input": "What's the latency like for https://langchain.com?"}
)

print(result)

if __name__ == "__main__":
    pass
