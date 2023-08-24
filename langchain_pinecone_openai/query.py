"""
This script is used to query pinecones database.
To load data into database, use the script langchain_pinecone.py
"""

from dotenv import load_dotenv,find_dotenv
from langchain.llms import OpenAI
# from langchain.schema import AIMessage, HumanMessage,SystemMessage
# from langchain.chat_models import ChatOpenAI
import os
# import openai
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
import pinecone
import openai
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


# load environment variables
load_dotenv(find_dotenv())
OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
PINECONE_ENV=os.environ["PINECONE_ENV"]
PINECONE_API_KEY=os.environ["PINECONE_API_KEY"]

# print("Authentication check")
# print(openai.Engine.list())

# constants
MODEL = 'text-embedding-ada-002'


# # load pdf file
# loader = UnstructuredFileLoader("Light_Prompt.pdf")
# data = loader.load()

# # split file 
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(data)
# texts = text_splitter.split_text(data)
# print("TEXTS: ", texts)
# embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)
index_name = "langchain1"
index = pinecone.Index(index_name)

# print("Docsearch: ",docsearch)

# get embeddings and then pass to pinecone
# docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
# docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

# starting question and answer chain on openai
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
# chain = load_qa_chain(llm, chain_type="stuff")

# Load query
filename3 = 'data/mqtt_message.txt'
with open(filename3, 'r') as f:
    query = f.read()

# embedding query
query_vector = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
# print("queryvector: ", len(query_vector))
# docs = docsearch.similarity_search(query)

# querying pinecone db to get relevant prompts
# top_k is to return k number of relevant searches
# include_metadata is to return the original data and not its vector form
result = index.query(vector=query_vector,top_k=3,include_metadata=True).matches
# print("result: ",result)
# print("query: ",query)

chain = load_qa_chain(llm, chain_type="stuff")
# print("chain: ", chain)
# passing all relevant prompts and documents from pinecone and passing it to GPT
print("Prompt has been sent. Waiting for response...")

# input_document type: list | question type: str
for i in range(5):
    response = chain.run(input_documents=result, question=query)
    # response = chain({"input_documents": result, "question": query}, return_only_outputs=True)
    print(response)