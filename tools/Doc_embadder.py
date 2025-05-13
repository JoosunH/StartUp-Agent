import os
import faiss
import json
from PyPDF2 import PdfReader
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer("all-mpnet-base-v2")

doc_chunks = []
doc_index = None

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    with open(pdf_path, "rb") as file:
        reader = PdfReader(pdf_path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
def chunk_text(text: str, max_words = 300, overlap =50) -> List[str]:
    """
    Instead the whole text we chunk it up maximum of 512 words. And each chunk get embedded separately.
    The reason we chunk it is:
    1.)Embedding smaller chunks (vs. whole pages or documents) = more precise search

    2.)PAvoids injecting irrelevant or bloated context into LLM

    3.)Works well with token limits in GPT prompt
    """
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words- overlap)]

def embed_and_index_chunks(chunks: List[str]):
    """
    Embed the text chunks and create a FAISS index.
    And doc_index represents the vector embedding of the text chunks.
    And doc_chunks represents the text chunks that are actually text/String.
    doc_
    """
    global doc_index, doc_chunks
    if not chunks:
        print("No chunks to embed and index.")
        return None
    
    embeddings = model.encode(chunks, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    
    doc_chunks = chunks
    doc_index = index
    
    return index

def search_uploaded_doc(query: str, k=3, threshold=0.8) -> str:
    if doc_index is None or doc_chunks is None:
        print("No document index available. Please process a document first.")
        return ""
    
    query_vector = model.encode([query], normalize_embeddings=True)
    D, I = doc_index.search(np.array(query_vector), k)
    
    results = []
    for dist, idx in zip(D[0], I[0]):
        if dist < threshold:
            chunk = doc_chunks[idx]
            results.append(f"(Score: {dist:.3f})\n{chunk}")
        else:
            print(f"🟡 Skipped weak chunk (distance = {dist:.3f})")
    if not results:
        print("No relevant chunks found.")
    return "\n---\n".join(results).strip()

def process_document(file_path: str):
    """
    Process a PDF document: extract text, chunk it, and create an index.
    """
    print(f"📄 Processing file: {file_path}")
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    embed_and_index_chunks(chunks)
    
    
    
# Example integration with agent
# if __name__ == "__main__":
#     file = "C:\\Users\\maccan47\\Desktop\\Project\\Startup agent\\LLM.pdf"  # Replace with actual uploaded path
#     process_document(file)

#     idea = "Creating innovative digital business models with the assistance of artificial intelligence technology."
#     context_from_doc = search_uploaded_doc(idea)
#     print("\n📚 Context from Uploaded Document:\n")
#     print(context_from_doc or "No relevant content found in document.")
    
#     """
#     "C:\\Users\\maccan47\\Desktop\\Project\\Startup agent\\The-Farmers-Dog-Plans-Book.pdf"
#     """