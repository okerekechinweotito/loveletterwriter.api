import datetime
import openai
from ..import models

class ChatBotBusiness:
    @staticmethod
    def chat_with_ai(user_id, item, db):
        # get current user
        found_name = db.query(models.User).filter(models.User.id == user_id).first()
        if not found_name:
            name = 'Anonymous'
        else:
            name = found_name.first_name

        # get previous chats
        found_all_chat = db.query(models.ChatBot).filter(models.ChatBot.user_id == user_id).all()
        if found_all_chat:
            history_chat = ''
            total_chat = 0
            for chat in found_all_chat:
                if total_chat == 0:
                    history_chat = history_chat+ "\n\nHuman: My name is '+name+'. Greet me and ask me how you can help me today.\nAI: "+str(chat.ai)
                else:
                    history_chat = history_chat+ "\n\nHuman: "+str(chat.human)+".\nAI: "+str(chat.ai)
                total_chat = total_chat + 1
            history_chat = history_chat + "\n\nHuman: "+str(item.question)+".\nAI:"
            gpt_prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."+history_chat
        else:
            chat_msg = 'My name is '+name+'. Greet me and ask me how you can help me today.'
            gpt_prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: "+chat_msg+".\nAI:"

        response2 = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        if response2['choices'][0]['text']:
            ai_response = response2['choices'][0]['text']
            response_object = {
                'status': 1,
                'answer': response2['choices'][0]['text'],
                'message': 'Letter was not generated. Please try again later.'
            }
        else:
            ai_response = 'Sorry, i dont know that answer.'
            response_object = {
                'status': 0,
                'answer': 'Sorry, i dont know that answer.',
                'message': 'Letter was not generated. Please try again later.'
            }
        if found_all_chat:
            human_ques = item.question
        else:
            human_ques = ''
        new_chat = models.ChatBot(
            user_id=user_id,
            human=human_ques,
            ai=ai_response,
            date_created=datetime.datetime.now()
        )
        db.add(new_chat)
        try:
            db.commit()
            db.refresh(new_chat)
        except Exception as e:
            print(str(e))

        return response_object
