from config import set_environment
from langchain.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

set_environment()

model = ChatOpenAI()

example_prompt = PromptTemplate(
    template="{input} -> {output}",
    input_variables=["input", "output"],
)
examples = [
    {
        "input": "I absolutely love the new update! Everything works seamlessly.",
        "output": "Positive",
    },
    {
        "input": "It's okay, but I think it could use more features.",
        "output": "Neutral",
    },
    {
        "input": "I'm disappointed with the service, I expected much better performance.",
        "output": "Negative",
    },
]

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)
print(
    (prompt | model).invoke({"input": "This is an excellent book with high quality explanations."})
)

selector = SemanticSimilarityExampleSelector.from_examples(
    examples=examples,
    embeddings=OpenAIEmbeddings(),
    vectorstore_cls=Chroma,
    k=4,
)
prompt = FewShotPromptTemplate(
    example_selector=selector,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)
print((prompt | model).invoke({"input": "What's 10+10?"}))


if __name__ == "__main__":
    pass
