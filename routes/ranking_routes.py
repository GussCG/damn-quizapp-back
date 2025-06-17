from typing import List

from fastapi import APIRouter, HTTPException

from models.ranking import Ranking
from services.ranking_service import get_ranking_for_category

router = APIRouter()


@router.get("/{categoria}", response_model=List[Ranking])
async def get_ranking(categoria: str):
    ranking = await get_ranking_for_category(categoria)
    if not ranking:
        raise HTTPException(
            status_code=404, detail="No hay resultados para esta categoría"
        )
    return ranking
