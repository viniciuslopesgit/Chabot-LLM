# Ragbot.io 🤖

![Captura de ecrã de 2025-01-15 13-05-32](https://github.com/user-attachments/assets/d054b1c3-0934-48b9-b927-31342ff71e99)

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
