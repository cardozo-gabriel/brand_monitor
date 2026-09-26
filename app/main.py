"""Ponto de entrada da aplicacao FastAPI."""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Brand Monitor")
app.include_router(router)