from config import set_environment

set_environment()

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

checkpoint = "Salesforce/codegen-350M-mono"
model = AutoModelForCausalLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
pipe = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=500
)
text = """
def calculate_primes(n):
    \"\"\"Create a list of consecutive integers from 2 up to N.

    For example:
    >>> calculate_primes(20)
    Output: [2, 3, 5, 7, 11, 13, 17, 19]
    \"\"\"
"""


if __name__ == "__main__":
    from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
    # Please note that for newer langchain versions you should change this import:
    # from langchain_huggingface.llms import HuggingFacePipeline
    llm = HuggingFacePipeline(pipeline=pipe)
    llm.invoke(text)
