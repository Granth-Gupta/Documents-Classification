from pypdf import PdfReader
import re

class PdfToText(object):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def pdf_to_text(self):
        reader = PdfReader(self.pdf_path)

        texts = ""
        for page in reader.pages:
            texts += page.extract_text()
        texts = re.sub(r"\n\s*\n", " \n", texts).strip()

        return texts