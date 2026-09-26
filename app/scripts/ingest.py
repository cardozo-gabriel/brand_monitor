"""Leitura e processamento do arquivo de respostas."""

import json
from pathlib import Path
from typing import Any

from app.services.data_cleaner import deduplicate_responses


def load_responses(
	file_path: str | Path = "respostas-exemplo.json",
) -> list[dict[str, Any]]:
	"""Carrega um JSON de respostas e elimina duplicatas identicas por ID."""
	path = Path(file_path)
	try:
		with path.open(encoding="utf-8") as responses_file:
			responses = json.load(responses_file)
	except json.JSONDecodeError as error:
		raise ValueError(f"O arquivo '{path}' nao contem um JSON valido.") from error

	if not isinstance(responses, list):
		raise ValueError(f"O arquivo '{path}' precisa conter uma lista de respostas.")

	return deduplicate_responses(responses)


def main() -> None:
	responses = load_responses()
	print(f"{len(responses)} respostas prontas apos remover duplicatas.")


if __name__ == "__main__":
	main()