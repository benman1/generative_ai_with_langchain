"""Question answering app in Streamlit.

Based on this template:
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

from config import set_environment
from question_answering.agent import load_agent

set_environment()

st.set_page_config(page_title="LangChain Question Answering", page_icon=":robot:")
st.header("Ask a research question!")

tool_names = st.multiselect(
    'Which tools do you want to use?',
    [
        "google-search", "ddg-search", "wolfram-alpha", "arxiv",
        "wikipedia", "python_repl", "pal-math", "llm-math"
    ],
    ["ddg-search", "wolfram-alpha", "wikipedia"])

agent_chain = load_agent(tool_names=tool_names)

st_callback = StreamlitCallbackHandler(st.container())

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_chain.run(prompt, callbacks=[st_callback])
        st.write(response)
