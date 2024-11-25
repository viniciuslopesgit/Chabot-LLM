import requests
import json
from pdf_chunk import load_txt, retrieve_best_chunk, chunk_text
from pdf_upload import pdf_extract

OLLAMA_URL = "http://172.17.0.3:11434"  # Endereço da instância do Ollama
MODEL_NAME = "qwen2:0.5b"  # Modelo configurado no Ollama

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
            print("\n >> Ollama: ", end="", flush=True)
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            print(data["message"]["content"], end="", flush=True)
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        print("Erro ao decodificar JSON:", flush=True)
            print()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se conectar ao Ollama: {e}")
        return "Erro na conexão com o servidor Ollama"

# Função principal
def main():
    pdf_extract()  # Extrai e salva o texto do PDF
    print(f"Bem-vindo ao assistente {MODEL_NAME}!")
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

