"""Prompt tracking with PromptWatch.io."""
from config import set_environment
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from promptwatch import PromptWatch

set_environment()

prompt_template = PromptTemplate.from_template("Finish this sentence: {input}")
llm = OpenAI()
my_chain = prompt_template | llm

with PromptWatch() as pw:
    my_chain.invoke({"input": "The quick brown fox jumped over"})

if __name__ == "__main__":
    pass
