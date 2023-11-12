"""Question answering app in Streamlit.

Originally based on this template:
https://github.com/hwchase17/langchain-streamlit-template/blob/master/main.py

Run locally as follows:
> PYTHONPATH=. streamlit run question_answering/app.py

Alternatively, you can deploy this on the Streamlit Community Cloud
or on Hugging Face Spaces. For Streamlit Community Cloud do this:
1. Create a github repo
2. Go to Streamlit Community Cloud, click on "New app" and select the new repo
3. Click "Deploy!"
"""
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler

from question_answering.agent import load_agent
from question_answering.utils import MEMORY

st.set_page_config(page_title="LangChain Question Answering", page_icon=":robot:")
st.header("Ask a research question!")

strategy = st.radio(
    "Reasoning strategy",
    ("plan-and-solve", "zero-shot-react", ))

tool_names = st.multiselect(
    'Which tools do you want to use?',
    [
        "google-search", "ddg-search", "wolfram-alpha", "arxiv",
        "wikipedia", "python_repl", "pal-math",
        "llm-math"
    ],
    ["ddg-search", "wolfram-alpha", "wikipedia"])
if st.sidebar.button("Clear message history"):
    MEMORY.chat_memory.clear()

avatars = {"human": "user", "ai": "assistant"}
for msg in MEMORY.chat_memory.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

agent_chain = load_agent(tool_names=tool_names, strategy=strategy)

assistant = st.chat_message("assistant")
if prompt := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(prompt)
    stream_handler = StreamlitCallbackHandler(assistant)
    with st.chat_message("assistant"):
        response = agent_chain.run({
            "input": prompt,
            "chat_history": MEMORY.chat_memory.messages
        }, callbacks=[stream_handler]
        )
