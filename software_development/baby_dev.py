"""Task planner and executor for software development."""

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.agents import Tool
from langchain.tools import DuckDuckGoSearchResults
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)

from config import set_environment
from software_development.python_developer import DEV_PROMPT, PythonDeveloper, PythonExecutorInput

set_environment()

todo_prompt = PromptTemplate.from_template(
    "You are a planner who is an expert at coming up with requirements, "
    "required functions, for a given objective. "
    "Use this when you need to break down a task into smaller chunks."
    "The output should be a list of the format {function name}: {requirements of the function}"
    "Come up with a list of needed functions for this objective: {objective}"
)
todo_llm = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=todo_prompt
)
# # , model_name="ada"
software_prompt = PromptTemplate.from_template(DEV_PROMPT)
# careful: if you have the wrong model spec, you might not get any code!
software_llm = LLMChain(
    llm=OpenAI(
        temperature=0,
        max_tokens=4000
    ),
    prompt=software_prompt
)
software_dev = PythonDeveloper(llm_chain=software_llm)

code_tool = Tool(
    name="PythonSoftwareEngineer",
    func=software_dev.run,
    description=(
        "Useful for writing Python code. "
        "Input: a task or function to write. "
        "Output: a Python code that solves the task. "
    ),
    args_schema=PythonExecutorInput
)
planner_tool = Tool(
    name="TODO",
    func=todo_llm.run,
    description=(
        "Useful for when you need to come up with requirements. "
        "Input: an objective to create a todo list for. "
        "Output: a todo list for that objective. "
        "Please be very clear what the objective is!"
    )
)
ddg_search = DuckDuckGoSearchResults()
tools = [
    code_tool,
    Tool(
        name="DDGSearch",
        func=ddg_search.run,
        description=(
            "Useful for research and understanding background of objectives. "
            "Input: an objective. "
            "Output: background information about the objective. "
        )
    )
]

PREFIX = """You are an agent designed to write python code.

Chat History:
{chat_history}

You have access to a python REPL, which you can use to execute python code. 
Once the code is complete and free of errors you are finished.
If it does not seem like you can write this code, just return "I struggle to implement this" as the answer.
"""
SUFFIX = """Begin! Your goal is to write software. If you get an error, debug your code and try again!"

Task: {input}
{agent_scratchpad}

"""

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# prompt = ZeroShotAgent.create_prompt(
#     tools, prefix=PREFIX,
#     suffix=SUFFIX, input_variables=["input", "agent_scratchpad", "chat_history"]
# )

llm = OpenAI()
planner = load_chat_planner(llm)
executor = load_agent_executor(
    llm,
    tools,
    verbose=True,
)
agent_executor = PlanAndExecute(
    planner=planner,
    executor=executor,
    verbose=True,
    handle_parsing_errors="Check your output and make sure it conforms!",
    return_intermediate_steps=True
)

# agent = ZeroShotAgent(
#     llm_chain=llm_chain,
#     allowed_tools=tool_names,
#     handle_parsing_errors="Check your output and make sure it conforms!",
# )
# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=agent, tools=tools, verbose=True
# )


# # Logging of LLMChains
# verbose = False
# # If None, it will never stop
# max_iterations = 3
# baby_agi = BabyAGI.from_llm(
#     llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
# )

# agent_executor = create_python_agent(
#     llm=OpenAI(temperature=0, max_tokens=1000),
#     tool=code_excution,
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )


if __name__ == "__main__":
    agent_executor.run("Write a tetris game in python!")
