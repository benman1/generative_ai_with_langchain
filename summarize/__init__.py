"""Create summaries from pdf files.

Given any pdf file or directory with pdf files,
create a summary and save it as a .txt file.
"""
import logging
import os
from pathlib import Path

import langchain
from langchain import LLMChain, PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document

from config import set_environment
from summarize import prompts

set_environment()
# cache for debugging - reset: rm .langchain.db
langchain.llm_cache = langchain.cache.SQLiteCache(database_path=".langchain.db")

CHAT = ChatOpenAI(
    temperature=0.7,
)
logging.basicConfig(encoding="utf-8", level=logging.INFO)
LOGGING = logging.getLogger()


def format_summary(summary: dict) -> str:
    """Format a summary into a single string."""
    summary_template = PromptTemplate(
        input_variables=["main_summary", "executive_summary", "analogy"],
        template="{main_summary}\nSUMMARY:\n{executive_summary}\nANALOGY: {analogy}"
    )
    return summary_template.format(
        main_summary="\n".join(summary["intermediate_steps"]),
        executive_summary=summary["output_text"],
        analogy=summary["analogy"]
    )


def load_pdf(pdf_file_path: str) -> list[Document]:
    """Read and split pdf document."""
    pdf_loader = PyPDFLoader(pdf_file_path)
    return pdf_loader.load_and_split()


def summarize_docs(
        docs: list[Document],
) -> str:
    """Summarize a list of Documents.

    Result is returned as dict with these keys:
    * 'intermediate_steps' (list[str]),
    * 'output_text' (str), and
    * 'analogy' (str)
    """
    chain = load_summarize_chain(
        CHAT,
        chain_type="map_reduce",
        map_prompt=PromptTemplate(input_variables=["text"], template=prompts.SUMMARY),
        combine_prompt=PromptTemplate(input_variables=["text"], template=prompts.HIGH_LEVEL),
        return_map_steps=True
    )
    summary = chain({"input_documents": docs})
    # only works if the model is OpenAI
    with get_openai_callback() as cb:
        llm_chain = LLMChain.from_string(
            llm=CHAT,
            template=prompts.ANALOGY
        )
        summary["analogy"] = llm_chain.predict(text=summary["output_text"])
        LOGGING.info(f"Total Tokens: {cb.total_tokens}")
        LOGGING.info(f"Prompt Tokens: {cb.prompt_tokens}")
        LOGGING.info(f"Completion Tokens: {cb.completion_tokens}")
        LOGGING.info(f"Total Cost (USD): ${cb.total_cost}")

    return format_summary(summary=summary)


def summarize_pdf(pdf_file_path: str) -> str:
    """Helper function for pdfs."""
    docs = load_pdf(pdf_file_path=pdf_file_path)
    return summarize_docs(docs)


def create_pdf_summary(pdf_file):
    """Given a directory, create a summary as txt file.

    If summary was already created, return previous output.
    """
    pdf_path = Path(pdf_file)
    output_file = pdf_path.with_suffix('.txt')
    if os.path.exists(output_file):
        LOGGING.info("Summary file already exists!")
        with open(output_file, "r") as f:
            return f.read()

    summary = summarize_pdf(
        pdf_file_path=pdf_file
    )
    # write output:
    with open(output_file, "w") as f:
        f.write(summary)

    LOGGING.info(summary)


def create_pdf_summaries(directory: str):
    for filename in os.listdir(directory):
        full_filename = os.path.join(directory, filename)
        if not Path(filename).suffix.endswith("pdf") or not os.path.isfile(full_filename):
            continue

        LOGGING.info(f"Creating summary for {filename}...")
        create_pdf_summary(full_filename)


if __name__ == "__main__":
    directory = "/Users/ben/Downloads/langchain book/chapter6/"
    create_pdf_summaries(directory=directory)
    # create_pdf_summary(
    #     "/Users/ben/Downloads/langchain book/resources/textbooks are all you need.pdf"
    # )
