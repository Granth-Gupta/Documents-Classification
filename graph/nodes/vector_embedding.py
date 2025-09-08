from types import NoneType
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from graph.nodes.doc_retriever import print_all_contents
from graph.nodes.doc_retriever import data_retriever

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
docs_path = project_path + "/assets/unstructured"
persist_vs = project_path + "/ChromaDB/"

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

def text_to_vectorstore(text: str, index: int):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    collection_name = f"vectors_{index}"
    base_meta = {"source": f"text_{index}", "collection_name": collection_name}

    docs = splitter.split_documents(
        [Document(page_content=text, metadata=base_meta)]
    )
    vector_store = Chroma.from_documents(
        documents=docs,
        collection_name=collection_name,
        embedding=embeddings,
        persist_directory=persist_vs,
    )
    print(f"Created Vector store: vectors_{index}")
    return vector_store

def fetch_vectorstore(index: int):
    name = f"vectors_{index}"
    try:
        return Chroma(
            collection_name=name,
            persist_directory=persist_vs,
            embedding_function=embeddings,
            create_collection_if_not_exists=False,
        )
    except Exception:
        return None

def texts_to_vector_stores():
    content = print_all_contents(docs_path)

    vector_stores = []
    for i, text in enumerate(content):
        v = text_to_vectorstore(text, i)
        vector_stores.append(v)

    return vector_stores

def retriever_vs(index: int):
    vector_store = fetch_vectorstore(index)
    retriever_i = vector_store.as_retriever()
    return retriever_i

if __name__ == "__main__":
    vs = fetch_vectorstore(2)
    print(type(vs))
    if type(vs) == NoneType:
        print("Vector store not found")
        print("Creating Vector store")
        content = data_retriever(docs_path+"/How-to guides - 🦜️🔗 LangChain.url")
        vs = text_to_vectorstore(content, 2)
        print(vs)
        vs = fetch_vectorstore(1)
        print(type(vs))
    else:
        print("Vector store found")

    # class 'NoneType'>
    # Vector store not found
    # Creating Vector Store
    # Created Vector Store: vectors_1
    # <langchain_chroma.vectorstores.Chroma object at 0x0000020C1C681970>
    # <class 'langchain_chroma.vectorstores.Chroma'>