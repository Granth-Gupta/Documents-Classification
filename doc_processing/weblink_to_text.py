from langchain_community.document_loaders import WebBaseLoader
import configparser
from pathlib import Path
import re
from bs4 import BeautifulSoup

class URLPathToText():
    def __init__(self, url_path: Path):
        self.url_path = url_path

    def url_to_text(self, url: str) -> str:
        loder = WebBaseLoader(url)
        pages = loder.load()

        data_url = ""
        for page in pages:
            data_url += page.page_content
        data_url = re.sub(r"\n\s*\n", " \n", data_url).strip()
        return data_url

    def url_extractor(self) -> str:
        parser = configparser.ConfigParser()
        parser.read(self.url_path, encoding="utf-8")
        url = parser.get("InternetShortcut", "URL", raw=True)
        return url

    def urlpath_to_text(self):
        url = self.url_extractor()
        data_url = self.url_to_text(url)
        return data_url