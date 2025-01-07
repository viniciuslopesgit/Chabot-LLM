@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                     @
@                                                     @
@   ___    _   _  _____  _____  ___    _____  _____   @
@  (  _`\ ( ) ( )(  _  )(_   _)(  _`\ (  _  )(_   _)  @
@  | ( (_)| |_| || (_) |  | |  | (_) )| ( ) |  | |    @
@  | |  _ |  _  ||  _  |  | |  |  _ <'| | | |  | |    @
@  | (_( )| | | || | | |  | |  | (_) )| (_) |  | |    @
@  (____/'(_) (_)(_) (_)  (_)  (____/'(_____)  (_)    @
@                                                     @
@                                                     @
@   _____  _      _      _____         _____          @
@  (  _  )( )    ( )    (  _  )/'\_/`\(  _  )         @
@  | ( ) || |    | |    | (_) ||     || (_) |         @
@  | | | || |  _ | |  _ |  _  || (_) ||  _  |         @
@  | (_) || |_( )| |_( )| | | || | | || | | |         @
@  (_____)(____/'(____/'(_) (_)(_) (_)(_) (_)         @
@                                                     @
@                                 by: Vinícius Lopes  @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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
    python3 -m venv menv
    source menv/bin/activate
    pip install -r requirements.txt
  
  Instale a versão usada do llm:
    ollama run qwen2:1.5b


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
