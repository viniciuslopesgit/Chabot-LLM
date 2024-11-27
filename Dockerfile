FROM ollama/ollama

WORKDIR /app

# Instalar dependências básicas e limpar o cache
RUN apt-get update && \
    apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 11434

CMD ["python3", "app.py"]