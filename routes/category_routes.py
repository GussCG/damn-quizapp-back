from fastapi import APIRouter, Query

from services.quiz_service import fetch_categories, fetch_questions

router = APIRouter()


@router.get("/")
def get_categories():
    return fetch_categories()


@router.get("/preguntas")
async def get_questions(
    category: str = Query(...), limit: int = Query(10), page: int = Query(1)
):
    return await fetch_questions(category, limit, page)
