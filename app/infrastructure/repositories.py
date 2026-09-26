"""Implementacoes de acesso ao banco de dados."""

from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import Session

from app.domain.schemas import ResponseSchema
from app.infrastructure.models import ResponseRecord


class ResponseRepository:
	"""Le e grava respostas, evitando duplicar IDs no SQLite."""

	def __init__(self, session: Session) -> None:
		self.session = session

	def save_many(self, responses: Iterable[dict[str, Any]]) -> tuple[int, int]:
		"""Retorna quantas respostas inseriu e quantas ja existiam."""
		inserted_count = 0
		skipped_count = 0
		responses_in_batch: dict[str, dict[str, Any]] = {}
		field_names = set(ResponseSchema.model_fields)

		try:
			for response in responses:
				normalized = ResponseSchema.model_validate(response).model_dump(mode="json")
				response_id = normalized["id"]

				batch_copy = responses_in_batch.get(response_id)
				if batch_copy is not None:
					if batch_copy != normalized:
						raise ValueError(
							f"O id '{response_id}' aparece com conteudos diferentes."
						)
					skipped_count += 1
					continue

				responses_in_batch[response_id] = normalized
				existing = self.session.get(ResponseRecord, response_id)
				if existing is not None:
					if existing.to_dict() != normalized:
						raise ValueError(
							f"O id '{response_id}' ja esta salvo com conteudo diferente."
						)
					skipped_count += 1
					continue

				values = {
					field_name: normalized[field_name]
					for field_name in field_names
				}
				values["extra_data"] = {
					key: value for key, value in normalized.items() if key not in field_names
				}
				self.session.add(ResponseRecord(**values))
				inserted_count += 1

			self.session.commit()
		except Exception:
			self.session.rollback()
			raise

		return inserted_count, skipped_count

	def list_all(self) -> list[ResponseRecord]:
		return list(self.session.query(ResponseRecord).order_by(ResponseRecord.id).all())