# Ragbot.io 🤖


### Min Requirements:
- System: Linux/Windows/Mac
- NVIDIA GTX 1660 6GB
- 16G RAM
- Python3.10.12
- Server Ollama

 ### Instructions:
- Upload the PDF files that you want the chatbot to be knowledgeable about regarding the subject to be imported into the model.
- It is crucial that the titles of the PDFs are relevant to the content of the PDF to be indexed.
- Interact normally with the chatbot.

 ### Manual install
 Create a local directory:
 ```
 git clone https://github.com/viniciuslopesgit/chatbot.git
 ```

Create a virtual environment:
```
python3 -m venv .menv
source .menv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

Install the used LLMs version:
```
ollama pull ''
```

Run the server
```
python3 app.py
```
