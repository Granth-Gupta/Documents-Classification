from graph.nodes.vector_embedding import (
    fetch_vectorstore,
    text_to_vectorstore
)
from graph.nodes.doc_retriever import data_retriever
from prompts.classification_prompt import SYSTEM, HUMAN
from langchain_core.runnables import RunnableParallel

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.retrievers import MergerRetriever
from types import NoneType
from dotenv import load_dotenv
from pathlib import Path
import sqlite3
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
docs_path = Path(project_path + "/assets/unstructured")
files = os.listdir(docs_path)

conn = sqlite3.connect('common_context.db')
cur = conn.cursor()

llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

qa_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM), ("human", HUMAN)]
)

def qa_chain(num_docs: int ,index: int):
    retriever = []
    agent_name = f"agent_{index // 7}"
    s_num = index
    for i in range(0, num_docs):
        collection_name = f"vectors_{index}"
        file_name = files[index]
        cur.execute(
            "INSERT INTO context (S_Num, File_Name, Collection_Name, Agent_Name, Class) VALUES (?,?,?,?,?);",
            (index,file_name, collection_name, agent_name, '')
        )

        conn.commit()

        vs = fetch_vectorstore(index)
        if (type(vs) == NoneType):
            print(f"Create collection {index}")
            text = data_retriever(str(docs_path) +"/"+ files[index])
            create_collection = text_to_vectorstore(text, index)
            retriever.append(create_collection.as_retriever())
        else:
            print(f"Collection vectors_{index} already exists")
            retriever.append(vs.as_retriever())
        index = index + 1

    # conn.close()

    # merge_retriever = MergerRetriever(retrievers=retriever)
    qa_chain = {}
    length = len(retriever)
    for i in range(s_num, s_num+length):
        qa_chain[f"{i}"] = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever[i-s_num],
            chain_type="stuff",
            chain_type_kwargs={"prompt": qa_prompt},
            return_source_documents=False,
        )
    chain = RunnableParallel(qa_chain)

    return chain

if __name__ == "__main__":
    # qa = qa_chain(num_docs=2, index=1)
    # # print(qa.invoke({"query": "Find what the context is about."}))
    # print(qa)

    vs = fetch_vectorstore(1)
    # print(vs._collection_name)
    retriever = vs.as_retriever()
    # VectorStoreRetriever keeps a reference to the vectorstore
    collection_name = getattr(getattr(retriever, "vectorstore", None), "_collection_name", None)
    print(collection_name)

