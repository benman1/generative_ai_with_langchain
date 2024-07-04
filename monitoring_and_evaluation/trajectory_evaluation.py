from langchain.evaluation import EvaluatorType, load_evaluator
from langchain_openai import OpenAI

eval_llm = OpenAI(temperature=0)
# GPT 4.0 by default:
evaluator = load_evaluator(evaluator=EvaluatorType.AGENT_TRAJECTORY, llm=eval_llm)
