 Chatbot


------------------------------------------------------------------------
 MIN REQUIREMENTS:
------------------------------------------------------------------------
	- System: Linux/Windows/Mac
	- NVIDIA GTX 1660 6GB
	- 16G RAM
	- Python3.10.12
	- Server Ollama

------------------------------------------------------------------------
 USER INSTRUCTIONS:
------------------------------------------------------------------------
 1. Upload the PDF files that you want the chatbot to be knowledgeable about regarding the subject to be imported into the model.
 2. It is crucial that the titles of the PDFs are relevant to the content of the PDF to be indexed.
 3. Interact normally with the chatbot.

--------------------------------------------------------------------------
 INSTALAÇÃO LOCAL:
-------------------------------------------------------------------------- 
 Crie um diretório local:

 mkdir app/

 Aceda a pasta:
  
    	cd app/
    	apt update
    	apt install python3 python3.10-venv pip gunicorn git -y

 Clone o repositório do Github:

	git clone https://github.com/viniciuslopesgit/chatbot.git
    	cd chatbot
  
 Crie um ambiente virtual:

    	python3 -m venv .menv
    	source .menv/bin/activate
    	pip install -r requirements.txt
  
 Instale a versão usada do llm:

	ollama run qwen2:1.5b
	nomic-embed-text

  Outras verificações:

    Ajuste o ip para o ip local do container

 RUN:

  	server gunicorn
	python3 -m gunicorn -b 0.0.0.0:5000 app:app --workers 4 --worker-class gevent & nginx
  	vim /etc/nginx/nginx.config



