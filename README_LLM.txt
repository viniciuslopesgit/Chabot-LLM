

 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
 $   ___    _   _  _____  _____  _____  _____  _____   $
 $  |  _`| | | | ||  _  ||_   _||  _  ||  _  ||_   _|  $
 $  | | |_|| |_| || (_) |  | |  | (_) || | | |  | |    $
 $  | |  _ |  _  ||  _  |  | |  |  _ <'| | | |  | |    $
 $  | |_| || | | || | | |  | |  | (_) || |_| |  | |    $
 $  |____/'|_| |_||_| |_|  |_|  |_____||_____|  |_|    $
 $                                                     $
 $                             2025 viníciuslopesgit   $
 $                                                     $
 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$




 -------------------------------------------------------------------------
 IMPORTANT LINKS:
-------------------------------------------------------------------------
 https://www.youtube.com/watch?v=TMaQt8rN5bE


-------------------------------------------------------------------------
 DOCUMENTAÇÃO:
-------------------------------------------------------------------------
 LANGSMITH:

 Uso do LangSmith é uma ferramenta que possibilita o acompanhamento e debug durante o desenvolvimento e deploy de produção de LLMS

	a. A aplicação possui dentro da sua .env as configurações.
	b. A chamada do LangSmith é feita a partir da página .py.
	c. A plataforma do LangSmith não requer LangChain framework. Os logs traces são feitos via API or através de Python, ou	Typescrip SDKs.

 NOMIC:
 Para liberar acesso ao Nomic, é preciso fazer login a partir do terminal com 'nomic login [token]'

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


----------------------------------------------------------------------------
 INSTALAÇÃO DOCKER-COMPOSE:
---------------------------------------------------------------------------- 
 docker compose up --build
 ollama run no container criado pelo compose


