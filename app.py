from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.category_routes import router as category_router
from routes.quiz_routes import router as quiz_router
from routes.ranking_routes import router as ranking_router

app = FastAPI(title="Quiz API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
app.include_router(ranking_router, prefix="/ranking", tags=["ranking"])


@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to the Quiz API!"}
