import requests
import json
import pymupdf
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Configurações do Ollama
OLLAMA_URL = "http://172.17.0.3:11434"  # Endereço da instância do Ollama
MODEL_NAME = "qwen2:0.5b"  # Modelo configurado no Ollama

# Inicializa o modelo para embeddings (usando o Sentence-BERT)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Extrai texto do ficheiro .pdf
def pdf_search_question():
    doc = pymupdf.open("pdf/pdf/manual_inst_6.0_PT.pdf")
    out = open("pdf/txt/output.txt", "wb")
    for page in doc:
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()

# Carrega o texto extraído do ficheiro .txt
def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Divide o texto em "chunks" de tamanho adequado
def chunk_text(text, max_chunk_size=3000):
    chunks = []
    while len(text) > max_chunk_size:
        break_point = text.rfind('\n', 0, max_chunk_size)
        if break_point == -1:
            break_point = max_chunk_size
        chunks.append(text[:break_point])
        text = text[break_point:].strip()
    if text:
        chunks.append(text)
    return chunks

# Função para obter embeddings dos chunks e da pergunta
def get_embeddings(text_list):
    return embedder.encode(text_list)

# Função para recuperar a melhor resposta com base nos embeddings
def retrieve_best_chunk(question, chunks):
    # Gera embeddings para a pergunta e para os chunks
    question_embedding = get_embeddings([question])[0]
    chunk_embeddings = get_embeddings(chunks)

    # Calcula a similaridade entre a pergunta e cada chunk
    similarities = cosine_similarity([question_embedding], chunk_embeddings)[0]

    # Encontra o chunk mais relevante com base na maior similaridade
    most_similar_chunk_index = np.argmax(similarities)
    return chunks[most_similar_chunk_index]

# Responde à pergunta com base no conteúdo extraído do PDF usando embeddings
def pdf_search_answer(path, question):
    text = load_txt(path)
    chunks = chunk_text(text)
    
    # Recupera o chunk mais relevante
    best_chunk = retrieve_best_chunk(question, chunks)
    
    # Cria o prompt para o Ollama com base no chunk relevante
    prompt = f"""
    Baseado no seguinte texto:
    {best_chunk}
    Responda à seguinte pergunta passo a passo de forma detalhada:
    {question}
    """
    answer = interagir_ollama_stream(prompt)
    return answer

# Envia uma pergunta ao servidor Ollama e processa a resposta em streaming
def interagir_ollama_stream(pergunta):
    url = f"{OLLAMA_URL}/api/chat"
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": pergunta}]
    }
    try:
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            result = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            result += data["message"]["content"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        print("Erro ao decodificar JSON:", line)
            return result
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar ao Ollama: {e}")
        return "Erro na conexão com o servidor Ollama"

# Função principal
def main():
    pdf_search_question()  # Extrai e salva o texto do PDF

    print(f"Bem-vindo ao assistente {MODEL_NAME}!")
    while True:
        pergunta = input("\nVocê: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o programa. Até logo!")
            break
        
        # Responde com base no conteúdo do PDF usando embeddings
        pdf_answer = pdf_search_answer("pdf/txt/output.txt", pergunta)
        print("\nOllama: ", pdf_answer)

if __name__ == "__main__":
    main()
