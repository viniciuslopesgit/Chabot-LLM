import os
import uuid
import pymupdf
import numpy
import chromadb
from chromadb.utils import embedding_functions
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

client = chromadb.PersistentClient(path="chromaDB")
collection_name = "pdf_embeddings"
if collection_name not in client.list_collections():
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction('all-MiniLM-L6-v2')
    )
else:
    collection = client.get_collection(
        name=collection_name,
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction('all-MiniLM-L6-v2')
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def chunk_text(text, max_chunk_size=2000):
    chunks = []
    while len(text) > max_chunk_size:
        break_point = text.rfind('\n', 0, max_chunk_size)
        if break_point == -1:
            break_point = max_chunk_size
        chunks.append(text[:break_point].strip())
        text = text[break_point:].strip()
    if text:
        chunks.append(text)
    return chunks

def make_embeddings(text, filename):
    for idx, chunk in enumerate(text):
        embedding = collection._embedding_function(chunk)
        store_ids = [] # Debug
        unique_id = str(uuid.uuid4())
        collection.add(
                ids=[f"{filename}_{unique_id}"],
                documents=[chunk],
                metadatas=[{"chunk_index": idx}],
                embeddings=[embedding[idx]],
        )

def pdf_extract(filepath):
    if not os.path.exists('pdf/txt/'):
        os.makedirs('pdf/txt/')
    doc = pymupdf.open(filepath)
    with open("pdf/txt/output.txt", "w", encoding="utf-8") as out:
        for page in doc:
            text = page.get_text()
            out.write(text)
            out.write("\n" + "="*80 + "\n")

