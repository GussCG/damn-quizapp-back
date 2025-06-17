from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException

from models.user import User
from services.user_service import get_user_from_supabase

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Token de autorización no proporcionado"
        )

    token = authorization.replace("Bearer ", "")
    user = await get_user_from_supabase(token)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
