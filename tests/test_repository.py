"""Testes de persistencia das respostas."""

import tempfile
import unittest
from pathlib import Path

from sqlalchemy.orm import Session

from app.infrastructure.database import create_database_engine, initialize_database
from app.infrastructure.models import ResponseRecord
from app.infrastructure.repositories import ResponseRepository
from app.scripts.ingest import ingest_file


def make_response(response_id: str, text: str = "Resposta") -> dict[str, object]:
	return {
		"id": response_id,
		"pergunta": "Pergunta de teste",
		"plataforma": "ChatGPT",
		"modelo": None,
		"resposta_texto": text,
		"data_hora": None,
		"sentimento": None,
	}


class ResponseRepositoryTests(unittest.TestCase):
	def setUp(self) -> None:
		self.temp_directory = tempfile.TemporaryDirectory()
		self.addCleanup(self.temp_directory.cleanup)
		database_path = Path(self.temp_directory.name) / "test.sqlite3"
		self.engine = create_database_engine(f"sqlite:///{database_path}")
		self.addCleanup(self.engine.dispose)
		initialize_database(self.engine)

	def test_persists_records_and_skips_identical_records_on_rerun(self) -> None:
		response = make_response("r1")
		with Session(self.engine) as session:
			repository = ResponseRepository(session)
			self.assertEqual(repository.save_many([response]), (1, 0))
			self.assertEqual(repository.save_many([response]), (0, 1))
			self.assertEqual(repository.list_all()[0].to_dict(), response)

	def test_preserves_extra_scraping_fields(self) -> None:
		response = make_response("r1")
		response["origem_coleta"] = {"pagina": 2}
		with Session(self.engine) as session:
			repository = ResponseRepository(session)
			repository.save_many([response])

			self.assertEqual(repository.list_all()[0].to_dict(), response)

	def test_rejects_conflicting_id_and_rolls_back_the_whole_batch(self) -> None:
		with Session(self.engine) as session:
			repository = ResponseRepository(session)
			repository.save_many([make_response("existing")])

			with self.assertRaisesRegex(ValueError, "ja esta salvo"):
				repository.save_many(
					[
						make_response("new"),
						make_response("existing", "Conteudo diferente"),
					]
				)

			self.assertEqual([item.id for item in repository.list_all()], ["existing"])

	def test_initialization_migrates_legacy_platform_aliases(self) -> None:
		legacy_response = make_response("legacy")
		legacy_response["plataforma"] = "chat-gpt"
		with Session(self.engine) as session:
			session.add(ResponseRecord(**legacy_response, extra_data={}))
			session.commit()

		initialize_database(self.engine)

		with Session(self.engine) as session:
			self.assertEqual(
				ResponseRepository(session).list_all()[0].plataforma,
				"ChatGPT",
			)

	def test_ingest_file_persists_the_example_into_sqlite(self) -> None:
		project_root = Path(__file__).resolve().parents[1]
		database_path = Path(self.temp_directory.name) / "ingest.sqlite3"

		result = ingest_file(
			project_root / "respostas.json",
			f"sqlite:///{database_path}",
		)

		self.assertEqual(result, (10, 10, 0))