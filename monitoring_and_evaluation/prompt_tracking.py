"""Prompt tracking with PromptWatch.io."""
from config import set_environment
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from promptwatch import PromptWatch

set_environment()

prompt_template = PromptTemplate.from_template("Finish this sentence {input}")
my_chain = LLMChain(llm=OpenAI(), prompt=prompt_template)

with PromptWatch() as pw:
    my_chain("The quick brown fox jumped over")

if __name__ == "__main__":
    pass
