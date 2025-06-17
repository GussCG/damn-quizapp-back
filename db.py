import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Faltan las variables de entorno SUPABASE_URL y SUPABASE_KEY en .env"
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
