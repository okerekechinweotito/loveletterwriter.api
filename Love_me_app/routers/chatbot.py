

@router.post('/')
def chatbot(payload:schemas.ChatBot):
    email = payload.email
    messages = payload.message
