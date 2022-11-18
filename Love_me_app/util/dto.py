from pydantic import BaseModel


class AIResponseTrainer(BaseModel):
    status: int
    message: str
    data: list


class TrainerValue(BaseModel):
    ai_trainer_id: int
    value: str


class TrainerValueUpdate(BaseModel):
    value: str