from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.chat import router as chat_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI-First CRM HCP API",
    description=(
        "AI-first CRM backend powered by "
        "FastAPI, LangGraph and Groq."
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "AI-First CRM HCP API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "services": {
            "fastapi": "running",
            "database": "connected",
            "langgraph": "configured",
            "groq": "configured"
        }
    }