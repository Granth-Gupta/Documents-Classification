from graph.nodes.vector_embedding import fetch_vectorstore
from prompts.classification_prompt import SYSTEM, HUMAN

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

qa_prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM), ("human", HUMAN)]
)

def qa_chain(index: int):
    vs = fetch_vectorstore(index)
    retriever = vs.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt},
        return_source_documents=False,
    )
    return qa
