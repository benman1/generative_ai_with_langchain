"""Streamlit app for data analysis.

Run like this:
> PYTHONPATH=. streamlit run data_science/indexing.py
"""
import streamlit as st

from data_science.agent import query_agent, create_agent


st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    agent = create_agent(data)
    response = query_agent(agent=agent, query=query)
    st.write(response)
