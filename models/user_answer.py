from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserAnswer(BaseModel):
    question_id: UUID
    user_answer: str
    is_correct: bool


class UserAnswerCreate(UserAnswer):
    pass


class UserAnswerResponse(UserAnswer):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
