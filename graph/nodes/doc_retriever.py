from OCR.imagetoText import ocr_readable
from doc_processing.weblink_to_text import URLPathToText
from doc_processing.pdf_to_text import PdfToText
from pathlib import Path
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
DOCS_PATH = project_path + "/assets/unstructured"

def data_retriever(path: str) -> str:
    doc_path = Path(path)
    extension = doc_path.suffix.lower()

    if extension == ".pdf":
        obj = PdfToText(doc_path)
        content = obj.pdf_to_text()
        return content
    elif extension in [".jpg", ".jpeg", ".png"]:
        texts = ocr_readable(str(doc_path))
        return texts
    elif extension == ".url":
        url_object = URLPathToText(doc_path)
        data = url_object.urlpath_to_text()
        return data
    else:
        raise TypeError("Unsupported file type")

def print_all_contents(path: str) -> List[str]:
    docs_path = Path(path)

    content = []
    for doc in docs_path.iterdir():
        text = data_retriever(str(doc))
        content.append(text)

    return content

if __name__ == "__main__":
    content = print_all_contents(DOCS_PATH)

    for i, text in enumerate(content):
        print(f"Document {i+1}: ", text[:200])
        print("\n")

