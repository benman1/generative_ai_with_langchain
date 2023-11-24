from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import set_environment

set_environment()

cot_instruction = "Let's think step by step!"
cot_instruction2 = "Explain your reasoning step-by-step. Finally, state the answer."
reasoning_prompt = "{question}\n" + cot_instruction
prompt = PromptTemplate(
  template=reasoning_prompt,
  input_variables=["question"]
)

model = ChatOpenAI()
chain = prompt | model
print(chain.invoke({
   "question": "There were 5 apples originally. I ate 2 apples. My friend gave me 3 apples. How many apples do I have now?",
}))


if __name__ == "__main__":
    pass
