import datetime

from ..import models


class AITrainerBusiness:

    @staticmethod
    def get_all_trainer(user_id, length, start, db):
        found_trainer = db.query(models.AiTrainer)
        found_trainers = found_trainer.offset(start).limit(length).all()
        total_rows = found_trainer.count()
        is_last_page = total_rows <= start + length

        list_trainers = []
        if found_trainers:
            list_trainers = []
            for trainer in found_trainers:
                list_trainers.append({
                    'id': trainer.id,
                    'ui_name': trainer.ui_name,
                    'ai_word': trainer.ai_word,
                    'date_created': str(trainer.date_created),
                })
            response_object = {
                'status': 1,
                'data': list_trainers,
                "recordsTotal": total_rows,
                "is_last_page": is_last_page,
                'message': 'Found trainer/survey.'
            }
            return response_object
        else:
            response_object = {
                'status': 0,
                'data': list_trainers,
                "recordsTotal": total_rows,
                "is_last_page": is_last_page,
                'message': 'No trainer/survey found.'
            }
            return response_object

    @staticmethod
    def store_trainer_value(user_id, item, receiver_id, db):
        new_trainer_value = models.AiTrainerValue(
            ai_trainer_id = item.ai_trainer_id,
            user_id=user_id,
            receiver_id=receiver_id,
            value=item.value,
            date_created=datetime.datetime.now()
        )
        db.add(new_trainer_value)
        try:
            db.commit()
            db.refresh(new_trainer_value)
            print(new_trainer_value)
            response_object = {
                'status': 1,
                'message': 'Answer saved.'
            }
            return response_object
        except Exception as e:
            print(str(e))
            response_object = {
                'status': 0,
                'message': 'An error occured while saving answer.'
            }
            return response_object

    @staticmethod
    def update_trainer_value(user_id, item,ai_trainer_id, receiver_id, db):
        found_trainer_value = db.query(models.AiTrainerValue)\
            .filter(models.AiTrainerValue.ai_trainer_id == ai_trainer_id,
                    models.AiTrainerValue.receiver_id == receiver_id,
                    models.AiTrainerValue.user_id == user_id).first()

        if found_trainer_value:
            found_trainer_value.value = item.value
            try:
                db.commit()
                response_object = {
                    'status': 1,
                    'message': 'Answer updated.'
                }
                return response_object
            except Exception as e:
                print(str(e))
                response_object = {
                    'status': 0,
                    'message': 'An error occured while updating answer.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Survey question not found.'
            }
            return response_object

    @staticmethod
    def delete_trainer_value(user_id, ai_trainer_id, receiver_id, db):
        found_trainer_value = db.query(models.AiTrainerValue) \
            .filter(models.AiTrainerValue.ai_trainer_id == ai_trainer_id,
                    models.AiTrainerValue.receiver_id == receiver_id,
                    models.AiTrainerValue.user_id == user_id).first()

        if found_trainer_value:
            try:
                db.query(models.AiTrainerValue) \
                    .filter(models.AiTrainerValue.ai_trainer_id == ai_trainer_id,
                            models.AiTrainerValue.receiver_id == receiver_id,
                            models.AiTrainerValue.user_id == user_id).delete(synchronize_session=False)
                db.commit()
                response_object = {
                    'status': 1,
                    'message': 'Answer deleted.'
                }
                return response_object
            except Exception as e:
                print(str(e))
                response_object = {
                    'status': 0,
                    'message': 'An error occurred while deleting answer.'
                }
                return response_object
        else:
            response_object = {
                'status': 0,
                'message': 'Survey question not found.'
            }
            return response_object


