"""Ponto de entrada da aplicacao FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.infrastructure.database import (
	DEFAULT_DATABASE_URL,
	create_database_engine,
	initialize_database,
)


def create_app(database_url: str = DEFAULT_DATABASE_URL) -> FastAPI:
	@asynccontextmanager
	async def lifespan(application: FastAPI) -> AsyncIterator[None]:
		engine = create_database_engine(database_url)
		initialize_database(engine)
		application.state.engine = engine
		try:
			yield
		finally:
			engine.dispose()

	application = FastAPI(title="Brand Monitor", lifespan=lifespan)
	application.include_router(router)
	return application


app = create_app()
