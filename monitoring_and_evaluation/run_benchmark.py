"""Test our agent against a benchmark dataset.

This uses Langsmith. Please set your LangSmith API key. See
create_benchmark to create the benchmark dataset.
"""
import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.smith import RunEvalConfig, run_on_dataset
from langsmith import Client

from config import set_environment

set_environment()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "My Project"

client = Client()
shared_dataset_name = "Reasoning and Bias"

llm = ChatOpenAI(model="gpt-4", temperature=0.0)


# Use constructor function to initialize for each input:
def construct_chain():
    return LLMChain.from_string(
        llm,
        template="Help out as best you can.\nQuestion: {input}\nResponse: ",
    )


evaluation_config = RunEvalConfig(
    evaluators=[
        # Arbitrary criterion as a key: value pair in the criteria dict:
        RunEvalConfig.Criteria({"helpfulness": "Is the response helpful?"}),
        RunEvalConfig.Criteria({"insightful": "Is the response carefully thought out?"})
    ]
)

prototype_results = run_on_dataset(
    client=client,
    dataset_name=shared_dataset_name,
    llm_or_chain_factory=construct_chain,
    evaluation=evaluation_config,
    verbose=True,
)

prototype_project_name = prototype_results["project_name"]

if __name__ == "__main__":
    pass
