import requests
import json
import numpy as np
from pdf_chunk import load_txt, retrieve_best_chunk, chunk_text
from pdf_upload import pdf_extract
from chat_history import update_history, get_conversation_context
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

OLLAMA_URL = "http://172.17.0.3:11434"  # Endereço da instância do Ollama
MODEL_NAME = "qwen2:1.5b"

# Calcula a similaridade entre a pergunta e o chunk
def calc_similarity(question, chunk):
    vectorizer = TfidfVectorizer()
    # Converte a pergunta e o chunk em vetores
    matrix = vectorizer.fit_transform([question, chunk])
    similarity = cosine_similarity(matrix[0], matrix[1])[0][0]
    return similarity

# Responde à pergunta com base no conteúdo extraído do PDF usando embeddings
def pdf_search_answer(path, question):
    text = load_txt(path)
    chunks = chunk_text(text)
    # Recupera o chunk mais relevante
    best_chunk = retrieve_best_chunk(question, chunks)
    conversation_context = get_conversation_context()
    # Inclui o histórico no cálculo da similaridade (aqui consideramos também o contexto da conversa)
    conversation_text = " ".join([entry["content"] for entry in conversation_context])  # Histórico como string
    extended_question = f"{conversation_text} {question}"  # Combina histórico com a nova pergunta
    similarity = calc_similarity(extended_question, best_chunk)  # Calcula similaridade com o histórico considerado
    
    print(f"Similaridade entre a pergunta e o chunk: {similarity:.4f}")
    
    # Cria o prompt para o Ollama com base no chunk relevante e no histórico
    if similarity >= 0.1:
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
    
    # Adiciona a pergunta no histórico de conversa
    conversation_context.append({"role": "user", "content": question})
    
    # Interage com o modelo Ollama e obtém a resposta
    answer = interagir_ollama_stream(prompt)
    
    # Atualiza o histórico com a resposta do modelo
    update_history(question, answer)
    
    return answer
    

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
        print(f"Enviando solicitação para {url} com payload: {payload}")
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            answer = ""
            print("\n >> Ollama: ", end="", flush=True)
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            print(data["message"]["content"], end="", flush=True)
                            answer += data["message"]["content"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        print("Erro ao decodificar JSON:", flush=True)
            print()
            return answer
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar ao Ollama: {e}")
        return "Erro na conexão com o servidor Ollama"

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
if __name__ == "__main__":
    main()
