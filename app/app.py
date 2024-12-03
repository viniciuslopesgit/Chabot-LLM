from flask import Flask, render_template, request, jsonify, session, Response, stream_with_context
import chatbot

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/ask", methods=["GET"])
def ask():
    user_message = request.args.get("message")
    if not user_message:
        return "data: Erro: Mensagem inválida.\n\n", 400

    def generate_response():
        try:
            answer_generator = chatbot.pdf_search_answer_stream("pdf/txt/output.txt", user_message)
            for chunk in answer_generator:
                if chunk.strip():
                    yield f"data: {chunk}\n\n"
                
        except Exception as e:
            yield f"data: Erro interno do servidor: {str(e)}\n\n"

    return Response(stream_with_context(generate_response()), content_type='text/event-stream')


def update_history_in_session(question, answer):
    if "history" not in session:
        session["history"] = []
    session["history"].append({"role": "user", "content": question})
    session["history"].append({"role": "bot", "content": answer})

def get_conversation_context_from_session():
    return session.get("history", [])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
