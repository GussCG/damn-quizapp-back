from typing import Optional

from db import supabase
from models.user import User


async def get_user_from_supabase(token: str) -> Optional[User]:
    try:
        response = supabase.auth.get_user(token)

        if not response or not response.user:
            return None

        user_data = response.user

        return User(
            id=user_data.id,
            email=user_data.email,
            full_name=(
                user_data.user_metadata.get("username", "")
                if user_data.user_metadata
                else ""
            ),
        )

    except Exception as e:
        print(f"Error fetching user from Supabase: {e}")
        return None
