from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Ranking(BaseModel):
    user_id: UUID
    categoria: str
    score: int
    total_questions: Optional[int] = None
    user_name: Optional[str] = None
    answered_at: Optional[datetime] = None
