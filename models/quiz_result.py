from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class QuizResult(BaseModel):
    categoria: str
    score: int
    total_questions: Optional[int] = None
    created_at: Optional[datetime] = None


class QuizResultCreate(QuizResult):
    pass


class QuizResultResponse(BaseModel):
    id: UUID

    class Config:
        orm_mode = True
