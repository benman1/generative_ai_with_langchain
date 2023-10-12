"""Test our agent against a benchmark dataset.

This uses Langsmith. Please create and set your LangSmith API key.
The run_benchmark module runs against this dataset.
"""
import os

from langsmith import Client

from config import set_environment

set_environment()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "My Project"

client = Client()
questions = [
    "A ship's parts are replaced over time until no original parts remain. Is it still the same ship? Why or why not?",
    # The Ship of Theseus Paradox
    "If someone lived their whole life chained in a cave seeing only shadows, how would they react if freed and shown the real world?",
    # Plato's Allegory of the Cave
    "Is something good because it is natural, or bad because it is unnatural? Why can this be a faulty argument?",
    # Appeal to Nature Fallacy
    "If a coin is flipped 8 times and lands on heads each time, what are the odds it will be tails next flip? Explain your reasoning.",
    # Gambler's Fallacy
    "Present two choices as the only options when others exist. Is the statement \"You're either with us or against us\" an example of false dilemma? Why?",
    # False Dilemma
    "Do people tend to develop a preference for things simply because they are familiar with them? Does this impact reasoning?",
    # Mere Exposure Effect
    "Is it surprising that the universe is suitable for intelligent life since if it weren't, no one would be around to observe it?",
    # Anthropic Principle
    "If Theseus' ship is restored by replacing each plank, is it still the same ship? What is identity based on?",
    # Theseus' Paradox
    "Does doing one thing really mean that a chain of increasingly negative events will follow? Why is this a problematic argument?",
    # Slippery Slope Fallacy
    "Is a claim true because it hasn't been proven false? Why could this impede reasoning?",  # Appeal to Ignorance
]

shared_dataset_name = "Reasoning and Bias"
# create dataset on LangSmith:
ds = client.create_dataset(
    dataset_name=shared_dataset_name, description="A few reasoning and cognitive bias questions",
)
for q in questions:
    client.create_example(inputs={"input": q}, dataset_id=ds.id)

if __name__ == "__main__":
    pass
