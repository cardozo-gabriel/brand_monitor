"""Testes para higienizacao de dados."""

import json
import tempfile
import unittest
from pathlib import Path

from app.scripts.ingest import load_responses
from app.services.data_cleaner import deduplicate_responses


class DeduplicateResponsesTests(unittest.TestCase):
	def test_removes_identical_records_with_the_same_id(self) -> None:
		first = {"id": "r1", "resposta_texto": "Acme"}
		duplicate = {"id": "r1", "resposta_texto": "Acme"}

		result = deduplicate_responses([first, duplicate])

		self.assertEqual(result, [first])

	def test_rejects_different_records_with_the_same_id(self) -> None:
		first = {"id": "r1", "resposta_texto": "Acme"}
		conflicting = {"id": "r1", "resposta_texto": "Zenith"}

		with self.assertRaisesRegex(ValueError, "conteudos diferentes"):
			deduplicate_responses([first, conflicting])

	def test_rejects_records_without_a_non_empty_string_id(self) -> None:
		with self.assertRaisesRegex(ValueError, "id de texto"):
			deduplicate_responses([{"id": "  "}])

	def test_load_responses_deduplicates_the_input_file(self) -> None:
		response = {"id": "r1", "resposta_texto": "Acme"}
		with tempfile.TemporaryDirectory() as temp_directory:
			file_path = Path(temp_directory) / "respostas.json"
			file_path.write_text(
				json.dumps([response, response]),
				encoding="utf-8",
			)

			result = load_responses(file_path)

		self.assertEqual(result, [response])

	def test_example_file_loads_ten_unique_responses(self) -> None:
		project_root = Path(__file__).resolve().parents[1]

		result = load_responses(project_root / "respostas-exemplo.json")

		self.assertEqual(len(result), 10)
		self.assertEqual(len({response["id"] for response in result}), 10)

	def test_load_responses_rejects_a_non_list_json_document(self) -> None:
		with tempfile.TemporaryDirectory() as temp_directory:
			file_path = Path(temp_directory) / "respostas.json"
			file_path.write_text('{"id": "r1"}', encoding="utf-8")

			with self.assertRaisesRegex(ValueError, "lista de respostas"):
				load_responses(file_path)


if __name__ == "__main__":
	unittest.main()