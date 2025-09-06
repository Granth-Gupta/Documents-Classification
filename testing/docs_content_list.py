from graph.nodes.doc_retriever import print_all_contents
from dotenv import load_dotenv
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
DOCS_PATH = project_path + "/assets/unstructured"

if __name__ == "__main__":
    content = print_all_contents(DOCS_PATH)

    for i, text in enumerate(content):
        print(f"Document {i+1}: ", text[:200])
        print("\n")

