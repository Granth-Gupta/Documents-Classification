from doc_processing.pdf_to_text import PdfToText
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
PDF_PATH = Path(project_path + "/assets/unstructured/File1.pdf")

if __name__ == "__main__":
    object = PdfToText(PDF_PATH)
    content = object.pdf_to_text()
    print(content[:300])