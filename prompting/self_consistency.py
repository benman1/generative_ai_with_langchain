from langchain import PromptTemplate, LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI

from config import set_environment

set_environment()

solutions_template = """
Generate {num_solutions} distinct answers to this question:
{question}

Solutions:
"""
solutions_prompt = PromptTemplate(
   template=solutions_template,
   input_variables=["question", "num_solutions"]
)
solutions_chain = LLMChain(
   llm=ChatOpenAI(),
   prompt=solutions_prompt,
   output_key="solutions"
)

consistency_template = """
For each answer in {solutions}, count the number of times it occurs. Finally, choose the answer that occurs most.

Most frequent solution: 
"""
consistency_prompt = PromptTemplate(
   template=consistency_template,
   input_variables=["solutions"]
)
consistency_chain = LLMChain(
   llm=ChatOpenAI(),
   prompt=consistency_prompt,
   output_key="best_solution"
)
answer_chain = SequentialChain(
   chains=[solutions_chain, consistency_chain],
   input_variables=["question", "num_solutions"],
   output_variables=["best_solution"]
)

print(answer_chain.run(
   question="Which year was the Declaration of Independence of the United States signed?",
   num_solutions="5"
))


if __name__ == "__main__":
    pass
