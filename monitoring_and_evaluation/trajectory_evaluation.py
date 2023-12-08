from langchain import OpenAI
from langchain.chat_models import ChatAnthropic
from langchain.evaluation import load_evaluator, EvaluatorType

eval_llm = OpenAI(temperature=0)
# GPT 4.0 by default:
evaluator = load_evaluator(
    evaluator=EvaluatorType.AGENT_TRAJECTORY,
    llm=eval_llm
)
