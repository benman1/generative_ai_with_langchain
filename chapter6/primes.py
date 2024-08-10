import os

from git import Repo
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# Clone the book repository from GitHub
repo_path = os.path.expanduser("~/Downloads/generative_ai_with_langchain")
repo = Repo.clone_from("https://github.com/benman1/generative_ai_with_langchain", to_path=repo_path)

# Load the Python code using LanguageParser
loader = GenericLoader.from_filesystem(
    repo_path,
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
)
documents = loader.load()

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=50, chunk_overlap=0
)
# Split the Document into chunks for embedding and vector storage
texts = python_splitter.split_documents(documents)

# ----------

# Store the documents in a vector store
db = Chroma.from_documents(texts, OpenAIEmbeddings())
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 8})

# Create a retrieval chain for Q&A over code
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    ("placeholder", "{chat_history}"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(ChatOpenAI(), prompt)
qa = create_retrieval_chain(retriever, document_chain)

# Ask a question about the RunnableBinding class
question = "What is a RunnableBinding?"
result = qa.invoke({"input": question})
print(result["answer"])
