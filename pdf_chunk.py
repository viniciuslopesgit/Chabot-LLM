from sklearn.metrics.pairwise import cosine_similarity
from pdf_upload import pdf_extract
import numpy as np
from sentence_transformers import SentenceTransformer

# Inicializa o modelo para embeddings (usando o Sentence-BERT)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Carrega o texto extraído do ficheiro .txt
def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Divide o texto em "chunks" de tamanho adequado
def chunk_text(text, max_chunk_size=1000):
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

# Função para obter embeddings dos chunks e da pergunta
def get_embeddings(text_list):
    return embedder.encode(text_list)

# Função para recuperar a melhor resposta com base nos embeddings
def retrieve_best_chunk(question, chunks, min_similarity=0.2):
    # Gera embeddings para a pergunta e para os chunks
    question_embedding = get_embeddings([question])[0]
    chunk_embeddings = get_embeddings(chunks)

    # Calcula a similaridade entre a pergunta e cada chunk
    similarities = cosine_similarity([question_embedding], chunk_embeddings)[0]
    filtered_similarities = [(i, sim) for i, sim in enumerate(similarities) if sim >= min_similarity]
    if filtered_similarities:
        most_similar_chunk_index = max(filtered_similarities, key=lambda x: x[1])[0]
    else:
        # Encontra o chunk mais relevante com base na maior similaridade
        most_similar_chunk_index = np.argmax(similarities)
    return chunks[most_similar_chunk_index]