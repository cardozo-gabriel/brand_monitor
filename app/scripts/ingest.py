"""Leitura e processamento do arquivo de respostas."""

import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.infrastructure.database import (
	DEFAULT_DATABASE_URL,
	create_database_engine,
	initialize_database,
)
from app.infrastructure.repositories import ResponseRepository
from app.services.data_cleaner import normalize_responses


def load_responses(
	file_path: str | Path = "respostas-exemplo.json",
) -> list[dict[str, Any]]:
	"""Carrega, valida e normaliza as respostas do arquivo JSON."""
	path = Path(file_path)
	try:
		with path.open(encoding="utf-8") as responses_file:
			responses = json.load(responses_file)
	except json.JSONDecodeError as error:
		raise ValueError(f"O arquivo '{path}' nao contem um JSON valido.") from error

	if not isinstance(responses, list):
		raise ValueError(f"O arquivo '{path}' precisa conter uma lista de respostas.")

	return normalize_responses(responses)


def ingest_file(
	file_path: str | Path = "respostas-exemplo.json",
	database_url: str = DEFAULT_DATABASE_URL,
) -> tuple[int, int, int]:
	"""Valida um arquivo e persiste suas respostas de forma idempotente."""
	responses = load_responses(file_path)
	engine = create_database_engine(database_url)
	try:
		initialize_database(engine)
		with Session(engine) as session:
			inserted_count, skipped_count = ResponseRepository(session).save_many(responses)
	finally:
		engine.dispose()

	return len(responses), inserted_count, skipped_count


def main() -> None:
	loaded_count, inserted_count, skipped_count = ingest_file()
	print(
		f"{loaded_count} respostas validas: {inserted_count} novas, "
		f"{skipped_count} ja estavam salvas."
	)


if __name__ == "__main__":
	main()