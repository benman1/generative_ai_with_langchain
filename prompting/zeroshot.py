from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from config import set_environment

set_environment()

model = ChatOpenAI()
prompt = PromptTemplate(input_variables=["text"], template="Classify the sentiment of this text: {text}")
chain = prompt | model
print(chain.invoke({"text": "I hated that movie, it was terrible!"}))


if __name__ == "__main__":
    pass
