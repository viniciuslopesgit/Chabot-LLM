import requests
import json
import numpy as np
from pdf_chunk import load_txt, retrieve_best_chunk, chunk_text
from pdf_upload import pdf_extract
from chat_history import update_history, get_conversation_context
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import app

OLLAMA_URL = "http://0.0.0.0:11434"  # Endereço da instância do Ollama
MODEL_NAME = "qwen2:1.5b"

# Calcula a similaridade entre a pergunta e o chunk
def calc_similarity(question, chunk):
    vectorizer = TfidfVectorizer()
    # Converte a pergunta e o chunk em vetores
    matrix = vectorizer.fit_transform([question, chunk])
    similarity = cosine_similarity(matrix[0], matrix[1])[0][0]
    return similarity

# Responde à pergunta com base no conteúdo extraído do PDF usando embeddings
def pdf_search_answer_stream(path, question):
    text = load_txt(path)
    chunks = chunk_text(text)
    best_chunk = retrieve_best_chunk(question, chunks)
    conversation_context = app.get_conversation_context_from_session()
    conversation_text = " ".join([entry["content"] for entry in conversation_context])
    extended_question = f"{conversation_text} {question}"
    similarity = calc_similarity(extended_question, best_chunk)
    
    if similarity >= 0.02:
        prompt = f"""
        Baseado no seguinte texto:
        {best_chunk}
        Histórico da conversa:
        {conversation_text}
        Responda à seguinte pergunta passo a passo de forma detalhada:
        {question}
        """
    else:
        prompt = f"""
        Histórico da conversa:
        {conversation_text}
        Responda à seguinte pergunta passo a passo de forma detalhada:
        {question}
        """
    
    conversation_context.append({"role": "user", "content": question})
    for chunk in interagir_ollama_stream(prompt):
        yield chunk


# Função para aplicar formatação HTML básica (exemplo)
def aplicar_formato_html(texto):
    # Exemplo simples: transformar partes do texto em negrito, itálico ou adicionar quebras de linha
    texto = texto.replace("\n", "<br>")  # Adiciona quebra de linha onde há novas linhas
    texto = texto.replace("**", "<b>").replace("**", "</b>")  # Exemplo de negrito
    texto = texto.replace("*", "<i>").replace("*", "</i>")  # Exemplo de itálico
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


# Função principal
def main():
    pdf_extract()  # Extrai e salva o texto do PDF
    print(f"\n!|||||||||||||||||||||Bem-vindo ao assistente virtual|||||||||||||||||||||!")
    while True:
        pergunta = input("\n >> Você: ")
        print()
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o programa. Até logo!")
            break
        # Responde com base no conteúdo do PDF usando embeddings
        pdf_search_answer("pdf/txt/output.txt", pergunta)