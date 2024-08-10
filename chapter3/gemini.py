from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI

from langchain import PromptTemplate, LLMChain

from config import set_environment

set_environment()


template = """Given this text, decide what is the issue the customer is concerned about. Valid categories are these:
* product issues
* delivery problems
* missing or late orders
* wrong product
* cancellation request
* refund or exchange
* bad support experience
* no clear reason to be upset

Text: {email}
Category:
"""
prompt = PromptTemplate(template=template, input_variables=["email"])

# If there is no env variable set for API key, you can pass the API key
# to the parameter `google_api_key` of the `ChatGoogleGenerativeAI` function:
# `google_api_key="key"`.
llm = GoogleGenerativeAI()
# alternatively:
# llm = ChatGoogleGenerativeAI(
#     model="gemini-pro",
#     temperature=0.7,
#     top_p=0.85
# )

llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

def respond_to_customer_email(customer_email: str):
    print(llm_chain.run(customer_email))






if __name__ == "__main__":
    # print(summary)
    pass
