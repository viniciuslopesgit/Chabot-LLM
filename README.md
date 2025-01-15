 Chatbot


-------------------------------------------------------------------------
 MIN REQUIREMENTS:
-------------------------------------------------------------------------
	- System: Linux/Windows/Mac
	- NVIDIA GTX 1660 6GB
	- 16G RAM
	- Python3.10.12
	- Server Ollama

-------------------------------------------------------------------------
 USER INSTRUCTIONS:
-------------------------------------------------------------------------
 1. Upload the PDF files that you want the chatbot to be knowledgeable about regarding the subject to be imported into the model.
 2. It is crucial that the titles of the PDFs are relevant to the content of the PDF to be indexed.
 3. Interact normally with the chatbot.

--------------------------------------------------------------------------
 LOCAL INSTALLATION:
-------------------------------------------------------------------------- 
 1. Create a local directory:
 	git clone https://github.com/viniciuslopesgit/chatbot.git

 2. Navigate to the folder
 cd chatbot
 
 3. Create a virtual environment:
 python3 -m venv .menv
 source .menv/bin/activate

 4. Install requirements:
 pip install -r requirements.txt

 5. Install the used LLMs version:
 ollama pull ''
 
 6. Run the server
 python3 app.py
  
