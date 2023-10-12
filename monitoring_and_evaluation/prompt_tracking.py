"""Prompt tracking with PromptWatch.io."""
from langchain import LLMChain, OpenAI, PromptTemplate
from promptwatch import PromptWatch

from config import set_environment

set_environment()

prompt_template = PromptTemplate.from_template("Finish this sentence {input}")
my_chain = LLMChain(llm=OpenAI(), prompt=prompt_template)

with PromptWatch() as pw:
    my_chain("The quick brown fox jumped over")

if __name__ == "__main__":
    pass
