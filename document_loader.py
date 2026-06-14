import os
import re
import pdfplumber
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langdetect import detect

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def clean_text(text):
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()

        # Skip empty lines or non-English lines
        if not line or not is_english(line):
            continue

        # Skip page numbers or lines that are only numbers/symbols
        if re.match(r'page\s*\d+', line.lower()) or re.match(r'^[\d\s\W_]+$', line):
            continue

        cleaned.append(line)

    return " ".join(cleaned)

def load_documents(doc_dir):
    documents = []
    print(f"📁 Looking in: {doc_dir}")

    for filename in os.listdir(doc_dir):
        full_path = os.path.join(doc_dir, filename)

        if filename.endswith(".pdf"):
            print(f"📄 Loading PDF: {full_path}")
            try:
                with pdfplumber.open(full_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            cleaned = clean_text(text)
                            if cleaned:
                                documents.append(Document(page_content=cleaned, metadata={"source": full_path, "page": i+1}))
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

        elif filename.endswith(".xlsx"):
            print(f"📊 Loading Excel: {full_path}")
            try:
                loader = UnstructuredExcelLoader(full_path)
                docs = loader.load()
                for doc in docs:
                    cleaned = clean_text(doc.page_content)
                    if cleaned:
                        doc.page_content = cleaned
                        documents.append(doc)
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

    print(f"✅ Loaded {len(documents)} cleaned documents.")
    return documents

def split_documents(documents, chunk_size=1100, chunk_overlap=250):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    return splitter.split_documents(documents)