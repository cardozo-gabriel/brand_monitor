"""Modelos Pydantic e validacao de dados."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResponseSchema(BaseModel):
	"""Formato validado de uma resposta coletada."""

	model_config = ConfigDict(extra="allow")

	id: str = Field(min_length=1)
	pergunta: str = Field(min_length=1)
	plataforma: str = Field(min_length=1)
	modelo: str | None
	resposta_texto: str
	data_hora: datetime | None
	sentimento: str | None

	@field_validator("id", "pergunta", "plataforma")
	@classmethod
	def strip_required_text(cls, value: str) -> str:
		value = value.strip()
		if not value:
			raise ValueError("Este campo nao pode ficar vazio.")
		return value

	@field_validator("data_hora", mode="before")
	@classmethod
	def parse_data_hora(cls, value: Any) -> Any:
		if value is None or isinstance(value, datetime):
			return value
		if not isinstance(value, str):
			return value

		value = value.strip()
		if not value:
			raise ValueError("Use null quando a data nao estiver disponivel.")

		try:
			return datetime.fromisoformat(value.replace("Z", "+00:00"))
		except ValueError:
			pass

		for date_format in ("%d/%m/%Y", "%Y/%m/%d"):
			try:
				return datetime.strptime(value, date_format)
			except ValueError:
				continue

		raise ValueError("Formato de data_hora invalido.")