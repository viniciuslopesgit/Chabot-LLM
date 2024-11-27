from flask import Flask, render_template, request, jsonify, session
import chatbot
import text_format

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    print(f"Mensagem recebida: {user_message}")
    if user_message:
        # Chama função pdf_search_answer
        answer = chatbot.pdf_search_answer("pdf/txt/output.txt", user_message)
        answer_formated = text_format.formatar_texto(answer)
        return jsonify({"response": answer_formated})
    else:
        return jsonify({"response": "Erro: Mensagem inválida."}), 400
    
def update_history_in_session(question, answer):
    if "history" not in session:
        session["history"] = []
    session["history"].append({"role": "user", "content": question})
    session["history"].append({"role": "bot", "content": answer})

def get_conversation_context_from_session():
    return session.get("history", [])


if "__main__" == __name__:
    app.run(debug=True, host="0.0.0.0")

