import datetime
from ..import models
import os
import openai
import random


class LetterBusiness:
    @staticmethod
    def generate_letter(user_id, receiver_id, db):
        prompt_word = ''
        # get all survey answers
        found_trainer_values = db.query(models.AiTrainerValue)\
            .filter(models.AiTrainerValue.receiver_id == receiver_id, models.AiTrainerValue.user_id == user_id).all()
        # check if survey answers were found
        if found_trainer_values:
            # loop and form the ai prompt with the survey questions and answers
            prompt_word = ' who '
            for value in found_trainer_values:
                found_trainer = db.query(models.AiTrainer).filter(models.AiTrainer.id == value.ai_trainer_id).first()
                if found_trainer:
                    prompt_word = prompt_word+found_trainer.ai_word+' '+value.value + ' and '
                    print(prompt_word)

        # get sender name
        sender = 'anonymous'
        found_user = db.query(models.User).filter(models.User.id == user_id).first()
        if found_user:
            sender = found_user.first_name + ' ' + found_user.last_name

        # get receiver name
        receiver = 'anonymous'
        found_receiver = db.query(models.Receiver).filter(models.Receiver.id == receiver_id, models.Receiver.user_id == user_id).first()
        if found_receiver:
            receiver = found_receiver.name

        openai.api_key = os.getenv("OPENAI_API_KEY")

        # ensure that each letter is not the same
        response1 = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Write 100 comma separated love words.",
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        prompt_love_words = ' '
        if response1['choices'][0]['text']:
            love_words = ''.join(response1['choices'][0]['text'].splitlines()).split(",")
            total_word = len(love_words)

            # only use 5 words from the list of love words
            length_word = 5
            if total_word < 5:
                length_word = total_word

            # combine all the 5 words into string
            rand_list = random.sample(range(0, total_word), length_word)
            for n in rand_list:
                prompt_love_words = prompt_love_words + love_words[n] + ','

            # remove last comma
            prompt_love_words.rstrip(',')

        # now generate the letter
        gpt_prompt = "Use these words ["+prompt_love_words+"] and write a love letter from " + sender + " to " + receiver + prompt_word+'date and time of letter is '+ str(datetime.datetime.now())
        response2 = openai.Completion.create(
            engine="text-davinci-002",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(gpt_prompt)
        print(response2['choices'][0]['text'].strip())
        if response2['choices'][0]['text']:
            new_letter = models.Letter(
                user_id=user_id,
                receiver_id=receiver_id,
                title=response2['choices'][0]['text'].strip().split('\n', 1)[0].rstrip(','),
                letter=response2['choices'][0]['text'].strip(),
                date_created=datetime.datetime.now()
            )
            db.add(new_letter)
            try:
                db.commit()
                db.refresh(new_letter)
                response_object = {
                    'status': 1,
                    'id' :new_letter.id, 
                    'letter': response2['choices'][0]['text'],
                    'message': 'Letter was generated and saved.'
                }
            except Exception as e:
                response_object = {
                    'status': 0,
                    'letter': response2['choices'][0]['text'],
                    'message': 'Letter was generated but was not saved. Please try again later'
                }
        else:
            response_object = {
                'status': 0,
                'message': 'Letter was not generated. Please try again later.'
            }
        return response_object

    @staticmethod
    def generate_custom_letter(user_id, item, db):
        # check that request params are not empty
        partner_name = 'anonymous'
        name = 'anonymous'
        relationship = 'friend'
        occasion = ''
        inscription = 'romantic'
        custom_words = 'live together'

        if item.partner_name:
            partner_name = item.partner_name
        found_user = db.query(models.User).filter(models.User.id == user_id).first()
        if found_user:
            name = found_user.first_name + ' ' + found_user.last_name
        if item.relationship:
            relationship = item.relationship
        if item.occasion:
            occasion = item.occasion
        if item.inscription:
            inscription = item.inscription

        if item.custom_words:
            custom_words = item.custom_words

        openai.api_key = os.getenv("OPENAI_API_KEY")

        # ensure that each letter is not the same
        response1 = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Write 50 unique comma separated love keywords.",
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        prompt_love_words = ' '
        if response1['choices'][0]['text']:
            love_words = ''.join(response1['choices'][0]['text'].splitlines()).split(",")
            total_word = len(love_words)

            # only use 5 words from the list of love words
            length_word = 5
            if total_word < 5:
                length_word = total_word

            # combine all the 5 words into string
            rand_list = random.sample(range(0, total_word), length_word)
            for n in rand_list:
                prompt_love_words = prompt_love_words + love_words[n] + ','

            # remove last comma
            prompt_love_words.rstrip(',')

        # form the prompt word for the AI trainer
        prompt_word = ' who is their '+relationship+' for their '+occasion

        prompt_word_ai = "Use these keywords [" + prompt_love_words + "] and this sentence ["+custom_words +"] and this inscription ["+inscription +"] to write a love letter from "\
                      + name + " to " + partner_name + prompt_word + '.'

        response2 = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_word_ai,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        if response2['choices'][0]['text']:
            new_letter = models.Letter(
                user_id=user_id,
                title=response2['choices'][0]['text'].strip().split('\n', 1)[0].rstrip(','),
                letter=response2['choices'][0]['text'].strip(),
                date_created=datetime.datetime.now()
            )
            db.add(new_letter)
            try:
                db.commit()
                db.refresh(new_letter)
                response_object = {
                    'status': 1,
                    'letter': response2['choices'][0]['text'],
                    'letter_id': new_letter.id,
                    'message': 'Letter was generated and saved.'
                }
            except Exception as e:
                response_object = {
                    'status': 0,
                    'letter': response2['choices'][0]['text'],
                    'letter_id': 0,
                    'message': 'Letter was generated but was not saved. Please try again later'
                }
        else:
            response_object = {
                'status': 0,
                'letter': '',
                'letter_id': 0,
                'message': 'Letter was not generated. Please try again later.'
            }
        return response_object

    @staticmethod
    def get_letter(user_id, letter_id, db):
        found_letter = db.query(models.Letter).filter(models.Letter.id == letter_id).first()
        if found_letter:
            response_object = {
                'status': 1,
                'id': found_letter.id,
                'title': found_letter.title,
                'letter': found_letter.letter,
                'date_created': str(found_letter.date_created),
                'message': 'Letter found.'
            }
        else:
            response_object = {
                'status': 0,
                'message': 'Letter not found'
            }
        return response_object

