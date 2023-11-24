from langchain import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from config import set_environment

set_environment()


solutions_template = """
Generate {num_solutions} distinct solutions for {problem}. Consider factors like {factors}.

Solutions:
"""
solutions_prompt = PromptTemplate(
   template=solutions_template,
   input_variables=["problem", "factors", "num_solutions"]
)
evaluation_template = """
Evaluate each solution in {solutions} by analyzing pros, cons, feasibility, and probability of success.

Evaluations:
"""
evaluation_prompt = PromptTemplate(
  template=evaluation_template,
  input_variables=["solutions"]
)
reasoning_template = """
For the most promising solutions in {evaluations}, explain scenarios, implementation strategies, partnerships needed, and handling potential obstacles. 

Enhanced Reasoning: 
"""
reasoning_prompt = PromptTemplate(
  template=reasoning_template,
  input_variables=["evaluations"]
)
ranking_template = """
Based on the evaluations and reasoning, rank the solutions in {enhanced_reasoning} from most to least promising.

Ranked Solutions:
"""
ranking_prompt = PromptTemplate(
  template=ranking_template,
  input_variables=["enhanced_reasoning"]
)

solutions_chain = LLMChain(
   llm=ChatOpenAI(),
   prompt=solutions_prompt,
   output_key="solutions"
)
evalutation_chain = LLMChain(
   llm=ChatOpenAI(),
   prompt=evaluation_prompt,
   output_key="evaluations"
)
reasoning_chain = LLMChain(
   llm=ChatOpenAI(),
   prompt=reasoning_prompt,
   output_key="enhanced_reasoning"
)
ranking_chain = LLMChain(
   llm=ChatOpenAI(),
   prompt=ranking_prompt,
   output_key="ranked_solutions"
)
tot_chain = SequentialChain(
   chains=[solutions_chain, evalutation_chain, reasoning_chain, ranking_chain],
   input_variables=["problem", "factors", "num_solutions"],
   output_variables=["ranked_solutions"]
)
print(tot_chain.run(
   problem="Prompt engineering",
   factors="Requirements for high task performance, low token use, and few calls to the LLM",
   num_solutions=3
))


if __name__ == "__main__":
    pass
