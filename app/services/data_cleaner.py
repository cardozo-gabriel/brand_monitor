"""Logica de higienizacao de dados."""

from collections.abc import Iterable
from typing import Any


def deduplicate_responses(
	responses: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
	"""Remove repeticoes identicas e rejeita conflitos entre IDs iguais."""
	unique_responses: list[dict[str, Any]] = []
	responses_by_id: dict[str, dict[str, Any]] = {}

	for position, response in enumerate(responses, start=1):
		if not isinstance(response, dict):
			raise ValueError(f"O registro {position} precisa ser um objeto JSON.")

		response_id = response.get("id")
		if not isinstance(response_id, str) or not response_id.strip():
			raise ValueError(f"O registro {position} precisa ter um id de texto.")

		existing_response = responses_by_id.get(response_id)
		if existing_response is not None:
			if existing_response != response:
				raise ValueError(
					f"O id '{response_id}' aparece em registros com conteudos diferentes."
				)
			continue

		responses_by_id[response_id] = response
		unique_responses.append(response)

	return unique_responses