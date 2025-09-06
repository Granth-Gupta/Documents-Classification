from doc_processing.weblink_to_text import URLPathToText
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

project_path = os.getenv("PROJECT_PATH")
URL_PATH = Path(project_path + "/assets/unstructured/Conceptual guide - 🦜️🔗 LangChain.url")

if __name__ == "__main__":
    url_object = URLPathToText(URL_PATH)
    data = url_object.urlpath_to_text()
    url = url_object.url_extractor()

    print("URL: ",url)
    print("Content (First 200 characters): ")
    print(data[:1000])