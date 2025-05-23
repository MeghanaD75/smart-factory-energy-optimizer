from PyPDF2 import PdfReader
from langchain.schema import Document

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def preprocess_documents(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    return [Document(page_content=raw_text)]
