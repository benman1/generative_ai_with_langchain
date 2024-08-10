from langchain_core.output_parsers import StrOutputParser
from config import set_environment

set_environment()
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

# Establishing a prompt and expected LLM
prompt = PromptTemplate.from_template("Tell me a joke about {topic}.")
llm = OpenAI()

# A chain combining prompt, LLM, and output parser
joke_about_light_bulbs = prompt | llm | StrOutputParser()

# Execute the chain to generate a joke about light bulbs
response = joke_about_light_bulbs.invoke({"topic": "light bulbs"})

print(response)

if __name__ == "__main__":
    # print(summary)
    pass
