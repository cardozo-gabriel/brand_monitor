"""Modelos relacionais usados na persistencia."""

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class ResponseRecord(Base):
	__tablename__ = "respostas"

	id: Mapped[str] = mapped_column(String, primary_key=True)
	pergunta: Mapped[str] = mapped_column(Text, nullable=False)
	plataforma: Mapped[str] = mapped_column(String, nullable=False)
	modelo: Mapped[str | None] = mapped_column(String, nullable=True)
	resposta_texto: Mapped[str] = mapped_column(Text, nullable=False)
	data_hora: Mapped[str | None] = mapped_column(String, nullable=True)
	sentimento: Mapped[str | None] = mapped_column(String, nullable=True)
	extra_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

	def to_dict(self) -> dict[str, Any]:
		response = {
			"id": self.id,
			"pergunta": self.pergunta,
			"plataforma": self.plataforma,
			"modelo": self.modelo,
			"resposta_texto": self.resposta_texto,
			"data_hora": self.data_hora,
			"sentimento": self.sentimento,
		}
		return {**self.extra_data, **response}