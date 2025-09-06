from graph.chains.classification import qa_chain

if __name__ == "__main__":
    chain = qa_chain(1)
    result = chain.invoke({"query": "What is main class for context provided."})
    print(result)
    print(result.get("result", result))