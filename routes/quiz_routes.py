from typing import List

from fastapi import APIRouter, Body, Header, HTTPException, Query

from models.quiz_result import QuizResult, QuizResultCreate, QuizResultResponse
from models.user_answer import UserAnswerCreate
from services.quiz_service import (
    create_quiz_result,
    get_user_quizzes_from_db,
    save_user_answers,
)

router = APIRouter()


@router.post("/submit/result", response_model=QuizResultResponse)
async def submit_quiz_result(
    quiz_data: QuizResultCreate,
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    access_token = authorization.removeprefix("Bearer ").strip()
    result_id = await create_quiz_result(quiz_data, access_token)
    return {"id": result_id}


@router.post("/submit/answers", response_model=List[dict])
async def submit_quiz_answers(
    result_id: str = Query(...),
    answers: List[UserAnswerCreate] = Body(...),
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    access_token = authorization.removeprefix("Bearer ").strip()
    saved = await save_user_answers(answers, result_id, access_token)
    return saved


# Obtener los quizzes hechos por un usuario
@router.get("/me", response_model=List[QuizResult])
async def get_user_quizzes(user_id: str = Query(...), authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    access_token = authorization.removeprefix("Bearer ").strip()
    quizzes = await get_user_quizzes_from_db(user_id, access_token)

    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found for this user")
    return quizzes
