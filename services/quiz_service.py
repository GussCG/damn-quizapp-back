import os
from typing import Dict, List
from uuid import UUID

import httpx
from dotenv import load_dotenv
from supabase import Client, create_client

from models.quiz_result import QuizResultCreate
from models.user_answer import UserAnswerCreate

load_dotenv()

API_URL = os.getenv("QUIZ_API_URL")
API_KEY = os.getenv("QUIZ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {"Authorization": API_KEY}


def get_supabase_client_with_token(access_token: str) -> Client:
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.auth.set_session(access_token, access_token)
    return client


def get_user_id_from_token(access_token: str) -> str:
    # Decodifica el JWT (puedes usar jwt.decode o el método que uses)
    # Aquí te pongo un ejemplo simplificado:
    import jwt

    payload = jwt.decode(access_token, options={"verify_signature": False})
    return payload.get("sub")  # o el claim que tenga el user ID


# Obtener las categorías de preguntas
def fetch_categories() -> List[Dict[str, str]]:
    return [
        {
            "id": "geography",
            "name": "Geografía",
            "description": "Explora el mundo a través de sus países, capitales, ríos, montañas y accidentes geográficos. Pon a prueba tus conocimientos sobre continentes, océanos, fronteras políticas, banderas y cultura geográfica. Ideal para quienes aman viajar, descubrir nuevos lugares o simplemente dominar el mapa mundial.",
        },
        {
            "id": "arts&literature",
            "name": "Arte y Literatura",
            "description": "Sumérgete en el mundo de la creatividad humana a través de la pintura, la música, la escultura, la literatura clásica y contemporánea. Responde preguntas sobre autores, movimientos artísticos, obras maestras y libros que marcaron época. Perfecta para los amantes de las humanidades y la expresión artística.",
        },
        {
            "id": "entertainment",
            "name": "Entretenimiento",
            "description": "Desde películas, series y música hasta celebridades, cultura pop y videojuegos, esta categoría abarca lo mejor del entretenimiento global. ¿Qué tanto sabes de tus actores, bandas, franquicias y éxitos favoritos? Ideal para cinéfilos, melómanos y seguidores de la cultura popular.",
        },
        {
            "id": "science&nature",
            "name": "Ciencia y Naturaleza",
            "description": "Explora los secretos del universo, la biología, la química, la física, la astronomía y el medio ambiente. Aprende sobre animales, plantas, teorías científicas, inventos y fenómenos naturales. Una categoría ideal para mentes curiosas y exploradores del conocimiento científico.",
        },
        {
            "id": "sports&leisure",
            "name": "Deportes y Ocio",
            "description": "Demuestra tu pasión por el deporte y el tiempo libre con preguntas sobre fútbol, baloncesto, tenis, olimpiadas y más. También incluye hobbies, juegos de mesa y actividades recreativas. Una mezcla ideal para quienes disfrutan competir, jugar y mantenerse activos.",
        },
        {
            "id": "history",
            "name": "Historia",
            "description": "Viaja al pasado para conocer los eventos, personajes y civilizaciones que moldearon nuestro presente. Desde guerras y revoluciones hasta descubrimientos e imperios, esta categoría abarca miles de años de historia mundial. Ideal para apasionados de los hechos históricos y las lecciones del tiempo.",
        },
    ]


# Obtener preguntas de una categoría específica
async def fetch_questions(category: str, limit: int = 10, page: int = 1) -> List[Dict]:
    params = {"category": category, "limit": limit, "page": page}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/questions", headers=HEADERS, params=params
        )
        response.raise_for_status()
        return response.json()


# Guardar el resultado del quiz en la base de datos (con token JWT)
async def create_quiz_result(quiz_result: QuizResultCreate, access_token: str) -> UUID:
    supabase = get_supabase_client_with_token(access_token)

    data = quiz_result.dict()
    data["user_id"] = get_user_id_from_token(access_token)

    data = {k: v for k, v in data.items() if v is not None}

    try:
        response = supabase.table("quiz_result").insert(data).execute()
        if not response.data:
            raise ValueError("No data returned from insert operation")

        return UUID(response.data[0]["id"])
    except Exception as e:
        raise ValueError(f"Error inserting quiz result: {str(e)}")


# Guardar las respuestas del usuario (no requiere token si RLS no está habilitado en esa tabla)
async def save_user_answers(
    user_answers: List[UserAnswerCreate], quiz_result_id: UUID, access_token: str
) -> List[Dict]:
    supabase = get_supabase_client_with_token(access_token)

    data = []
    for answer in user_answers:
        data.append(
            {
                "quiz_result_id": str(quiz_result_id),
                "question_id": str(answer.question_id),
                "user_answer": answer.user_answer,
                "is_correct": answer.is_correct,
            }
        )

    try:
        response = supabase.table("user_answer").insert(data).execute()
        if not response.data:
            raise ValueError("No data returned from insert operation")

        return response.data
    except Exception as e:
        raise ValueError(f"Error inserting user answers: {str(e)}")


async def get_user_quizzes_from_db(user_id: str, access_token: str) -> List[Dict]:
    supabase = get_supabase_client_with_token(access_token)

    try:
        response = (
            supabase.table("quiz_result").select("*").eq("user_id", user_id).execute()
        )
        if not response.data:
            return []

        return response.data
    except Exception as e:
        raise ValueError(f"Error fetching user quizzes: {str(e)}")
