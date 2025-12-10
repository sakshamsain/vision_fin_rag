# app/main.py
from fastapi import FastAPI
from .api import router as api_router

app = FastAPI(title="Vision-First Financial RAG")

app.include_router(api_router, prefix="/api")
