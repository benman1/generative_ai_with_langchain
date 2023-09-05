"""Create an agent executor to use in the research app.

TODO: make sure history is maintained and used in conversation!
"""
from typing import Literal

from langchain import LLMChain, PromptTemplate
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor
from langchain_experimental.plan_and_execute.planners.base import LLMPlanner
from langchain_experimental.plan_and_execute.planners.chat_planner import PlanningOutputParser, load_chat_planner

from config import set_environment

set_environment()

PREFIX = "You are a helpful AI bot that's good at research and very reliable. " \
         "If you are not sure or don't have information, try to verify.\n" \
         "Previous history: {chat_history}\n"

PLANNER_PROMPT = (
    "Previous history: {chat_history}\n"
    "Let's first understand the problem and devise a plan to solve the problem."
    " Look up information using tools if necessary!"
    " Please output the plan starting with the header 'Plan:' "
    "and then followed by a numbered list of steps. "
    "Please make the plan the minimum number of steps required "
    "to accurately complete the task. If the task is a question, "
    "the final step should almost always be 'Given the above steps taken, "
    "please respond to the users original question'. "
    "At the end of your plan, say '<END_OF_PLAN>'"
)
PREFIX_WITH_TOOLS = PREFIX + "Look up the information using tools if necessary!\n"

INSTRUCTION = "Try to answer this question: {input}."

ReasoningStrategies = Literal["one-shot-react", "plan-and-solve"]

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
            template=PREFIX + INSTRUCTION,
            input_variables=["input", "chat_history"]
        ))

    tools = load_tools(
        tool_names=tool_names,
        llm=llm
    )
    if strategy == "plan-and-solve":
        planner = load_chat_planner(llm=llm, system_prompt=PLANNER_PROMPT)
        # llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        executor = load_agent_executor(llm, tools, verbose=True)
        return PlanAndExecute(
            planner=planner,
            executor=executor,
            verbose=True,
            handle_parsing_errors="Check your output and make sure it conforms!"
        )

    # Occasionally, we might come across a output parsing error.
    # We can handle these by setting "handle_parsing_errors"
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        agent_kwargs={
            "prefix": PREFIX_WITH_TOOLS,
            #"memory_prompts": [CHAT_HISTORY],
            "input_variables": ["input", "agent_scratchpad", "chat_history"]
        },
        #memory=MEMORY,
        verbose=True,
        handle_parsing_errors="Check your output and make sure it conforms!"
    )
