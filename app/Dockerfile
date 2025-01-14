# Usar a imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expôr a porta para Flask
EXPOSE 15991

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=15991"]

