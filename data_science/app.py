"""Streamlit app for data analysis.

Run like this:
> PYTHONPATH=. streamlit run data_science/indexing.py
"""
import streamlit as st

from data_science.agent import query_agent, create_agent


st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

data_file = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    assert data_file is not None
    agent = create_agent(data_file.getvalue().decode())
    response = query_agent(agent=agent, query=query)
    st.write(response)
