import datetime
import openai

class ChatBotBusiness:
    @staticmethod
    def chat_with_ai(user_id, item, db):
        gpt_prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: "+item.question+".\nAI:"
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
        print(gpt_prompt)
        print(response2['choices'][0]['text'].strip())
        if response2['choices'][0]['text']:
            response_object = {
                'status': 1,
                'answer': response2['choices'][0]['text'],
                'message': 'Letter was not generated. Please try again later.'
            }
        else:
            response_object = {
                'status': 0,
                'answer': 'Sorry, i dont know that answer.',
                'message': 'Letter was not generated. Please try again later.'
            }
        return response_object
