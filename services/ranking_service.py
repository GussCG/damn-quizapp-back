import asyncio
from typing import List

from db import supabase
from models.ranking import Ranking


async def get_ranking_for_category(categoria: str) -> List[Ranking]:
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: supabase.rpc(
                "get_best_scores_by_user", {"target_categoria": categoria}
            ).execute(),
        )
        data = response.data
        return [Ranking(**row) for row in data]
    except Exception as e:
        print(f"Error al obtener ranking: {e}")
        return []
