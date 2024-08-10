from langchain.llms.fake import FakeListLLM
from langchain.agents import create_react_agent
from langchain.agents import Tool
from langchain_core.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()


repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)
responses = ["Action: Python_REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
llm = FakeListLLM(responses=responses)

prompt = PromptTemplate.from_template(
    template='''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''
)
agent = create_react_agent(
    llm, [repl_tool], prompt
)



if __name__ == "__main__":
    # print(python_repl.run("print(1+1)"))
    # prompt.format(foo="bar")
    llm.invoke("what's 2 + 2")
