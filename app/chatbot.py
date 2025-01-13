import requests
import json
import numpy as np
from pdf_chunk import  retrieve_best_chunk, chunk_text
from chat_history import update_history, get_conversation_context
import app
import re

OLLAMA_URL = "http://0.0.0.0:11434"  # Endereço da instância do Ollama
MODEL_NAME = "qwen2:1.5b"

# Calcula a similaridade entre a pergunta e o chunk
def calc_similarity(user_message, top_k=3):
    query_embedding = collection._embedding_function(user_message)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results

# Responde à pergunta com base no conteúdo extraído do PDF usando embeddings
def pdf_search_answer_stream(chunks, question):

    print(f"\n\n\nChunks recebidos +ara a pergunta: {question}\n\n\n")
    print(f"Chunks: {chunks}")
    prompt = f"""
    Baseado no seguinte texto:
    {chunks}
    Responda à seguinte pergunta passo a passo de forma detalhada:
    {question}
    """
    
    for chunk in interagir_ollama_stream(prompt):
        yield chunk

# Função para aplicar formatação HTML (com fundo preto para blocos de código)
def aplicar_formato_html(texto):
    # Adiciona quebras de linha no lugar de "\n"
    texto = texto.replace("\n", "<br>")
    # Formatação de negrito, substituindo ** por <b></b>
    texto = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", texto)
    # Formatação de itálico, substituindo * por <i></i>
    texto = re.sub(r"\*(.*?)\*", r"<i>\1</i>", texto)

    return texto

# Envia uma pergunta ao servidor Ollama e processa a resposta em streaming
def interagir_ollama_stream(pergunta):
    url = f"{OLLAMA_URL}/api/chat"
    if isinstance(pergunta, str):
        pergunta = [{"role": "user", "content": pergunta}]
    payload = {
        "model": MODEL_NAME,
        "messages": pergunta
    }
    try:
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            part = data["message"]["content"]
                            formatted_part = aplicar_formato_html(part)  # Aplica formatação HTML
                            print(formatted_part, end="", flush=True)  # Imprime o texto formatado
                            yield formatted_part
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        yield "Erro ao decodificar JSON."
    except requests.exceptions.RequestException as e:
        yield f"Erro ao se conectar ao Ollama: {e}"

