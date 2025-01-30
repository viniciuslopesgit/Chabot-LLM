# Ragbot.io 🤖

![Captura de ecrã de 2025-01-15 13-05-32](https://github.com/user-attachments/assets/d054b1c3-0934-48b9-b927-31342ff71e99)

Ragbot is a smart chatbot that uses RAG (Retrieval-Augmented Generation) technology. It was built with Flask for the API, Ollama LLM for generating the responses, and ChromaDB for storing and retrieving data extracted from PDFs. The concept is simple: the user uploads a PDF, the system extracts the text, and stores it in ChromaDB. When someone asks a question, Ragbot searches for the most relevant excerpts in the database and uses them to generate a highly accurate response.

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
install ollama
ollama pull ''
```

Run the server
```
python3 app.py
```
