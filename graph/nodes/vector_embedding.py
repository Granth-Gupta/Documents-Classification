from langchain_chroma import Chroma            # new wrapper
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pathlib import Path
import os
from graph.nodes.doc_retriever import print_all_contents

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
docs_path = project_path + "/assets/unstructured"
persist_vs = project_path + "/ChromaDB/"

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

def text_to_vectorstore(text: str, index: int):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)  # returns Documents via split_documents [21]
    docs = splitter.split_documents([Document(page_content=text, metadata={"source": f"text_{index}"})])

    vector_store = Chroma.from_documents(
        documents=docs,
        collection_name=f"vectors_{index}",
        embedding=embeddings,
        persist_directory=persist_vs,
    )
    return vector_store

def fetch_vectorstore(index: int):
    return Chroma(
        collection_name=f"vectors_{index}",
        persist_directory=persist_vs,
        embedding_function=embeddings,
    )

def texts_to_vector_stores(path: str):
    content = print_all_contents(path)
    path = Path(path)

    vector_stores = []
    for i, text in enumerate(content):
        v = text_to_vectorstore(text, i)
        vector_stores.append(v)

    return vector_stores

def retriever_vs(index: int):
    vector_store = fetch_vectorstore(index)
    retriever_i = vector_store.as_retriever()
    return retriever_i
