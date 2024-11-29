# Escolher a imagem base com Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requirements.txt e instalá-los
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação Flask para o container
COPY . /app/

# Expor a porta que o Flask vai escutar
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "4", "--worker-class", "gevent"]
