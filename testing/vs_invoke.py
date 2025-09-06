from graph.nodes.vector_embedding import fetch_vectorstore
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

if __name__ == "__main__":
    vs = fetch_vectorstore(1)
    retriever_1 = vs.as_retriever()
    result = retriever_1.invoke("What is C++")
    print(result)
    raw = vs._collection.get(include=["documents", "metadatas"])  # columnar lists [19]
    print(f"count={len(raw.get('ids', []))}")

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever_1,
    )
    result = qa.invoke("What is C++")
    print(result)