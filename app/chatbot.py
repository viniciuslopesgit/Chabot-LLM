import requests
import json
import numpy as np
import app
import re

OLLAMA_URL = ""
MODEL_NAME = ""

def calc_similarity(user_message, top_k=3):
    query_embedding = collection._embedding_function(user_message)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results

def pdf_search_answer_stream(chunks, question):
    prompt = f"""
    {chunks}
    {question}
    """ 
    for chunk in interagir_ollama_stream(prompt):
        yield chunk

def aplicar_formato_html(texto):
    texto = texto.replace("\n", "<br>")
    texto = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"\*(.*?)\*", r"<i>\1</i>", texto)
    return texto

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
                            formatted_part = aplicar_formato_html(part)
                            yield formatted_part
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        yield "Erro ao decodificar JSON."
    except requests.exceptions.RequestException as e:
        yield f"Erro ao se conectar ao Ollama: {e}"

