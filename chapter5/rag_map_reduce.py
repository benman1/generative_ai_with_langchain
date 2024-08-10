from langchain.memory import ConversationSummaryMemory
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader, DirectoryLoader


qa_template = """
Use the following information from the context (separated with <ctx></ctx>) to answer the question.
Answer in German only, because the user does not understand English! \
If you don't know the answer, answer with "Unfortunately, I don't have the information." \
If you don't find enough information below, also answer with "Unfortunately, I don't have the information." \
------
<ctx>
{context}
</ctx>
------
<hs>
{chat_history}
</hs>
------
{question}
Answer:
"""

prompt = PromptTemplate(template=qa_template,
                            input_variables=['context','history', 'question'])
combine_custom_prompt='''
Generate a summary of the following text that includes the following elements:

* A title that accurately reflects the content of the text.
* An introduction paragraph that provides an overview of the topic.
* Bullet points that list the key points of the text.
* A conclusion paragraph that summarizes the main points of the text.

Text:`{context}`
'''


combine_prompt_template = PromptTemplate(
    template=combine_custom_prompt,
    input_variables=['context']
)

chain_type_kwargs={
        "verbose": True,
        "question_prompt": prompt,
        "combine_prompt": combine_prompt_template,
        "combine_document_variable_name": "context",
        "memory": ConversationSummaryMemory(
            llm=OpenAI(),
            memory_key="history",
            input_key="question",
            return_messages=True)
}

loader = DirectoryLoader("MY_PATH_TO_PDF_FILES",
                         glob='*.pdf',
                         loader_cls=PyPDFLoader)
documents = loader.load()

# This text splitter is used to create the parent documents - The big chunks
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)

# This text splitter is used to create the child documents - The small chunks
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)


bge_embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
    query_instruction=""

)

# The vectorstore to use to index the child chunks
from chromadb.errors import InvalidDimensionException
try:
    vectorstore = Chroma(collection_name="split_parents", embedding_function=bge_embeddings, persist_directory="chroma_db")
except InvalidDimensionException:
    Chroma().delete_collection()
    vectorstore = Chroma(collection_name="split_parents", embedding_function=bge_embeddings, persist_directory="chroma_db")


# The storage layer for the parent documents
store = InMemoryStore()

big_chunks_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

refine = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="map_reduce",
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs,
    retriever=big_chunks_retriever,
    verbose=True
)
