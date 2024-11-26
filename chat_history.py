conversation_history = []

def update_history(user_message, bot_response):
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "chatbot", "content": bot_response})
    #print(f"\n {user_message}")
    #print(f"\n {bot_response}")

def get_conversation_context():
    return conversation_history[-3:]