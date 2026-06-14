# build_vector_store.py

from document_loader import load_documents, split_documents
from vector_store import create_vector_store, save_vector_store
import os

# Path to document folder and FAISS index output
DOCS_PATH = r"C:\Users\super\OneDrive\Documents\Desktop\CampusFlow\docs"
INDEX_SAVE_PATH = "faiss_index"

def main():
    if not os.path.exists(DOCS_PATH):
        raise FileNotFoundError(f"📁 Document folder not found: {DOCS_PATH}")

    # Step 1: Load documents
    docs = load_documents(DOCS_PATH)
    print(f"📚 Loaded {len(docs)} documents.")

    # Step 2: Split into smaller chunks
    chunks = split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks.")

    # Step 3: Create FAISS vector store
    vector_store = create_vector_store(chunks)

    # Step 4: Save FAISS index locally
    save_vector_store(vector_store, INDEX_SAVE_PATH)
    print("✅ FAISS vector store saved successfully.")

if __name__ == "__main__":
    main()