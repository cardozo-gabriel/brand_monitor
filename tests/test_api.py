"""Testes dos endpoints HTTP."""

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app

def make_payload(
	response_id: str,
	text: str,
	platform: str = "ChatGPT",
) -> dict[str, object]:
	return {
		"id": response_id,
		"pergunta": "Pergunta de teste",
		"plataforma": platform,
		"modelo": None,
		"resposta_texto": text,
		"data_hora": None,
		"sentimento": None,
	}

class ApiTests(unittest.TestCase):
	def setUp(self) -> None:
		self.temp_directory = tempfile.TemporaryDirectory()
		self.addCleanup(self.temp_directory.cleanup)
		database_path = Path(self.temp_directory.name) / "api.sqlite3"
		self.client_context = TestClient(create_app(f"sqlite:///{database_path}"))
		self.client = self.client_context.__enter__()
		self.addCleanup(self.client_context.__exit__, None, None, None)

	def test_share_of_voice_returns_total_and_platform_percentages(self) -> None:
		self.client.post("/respostas", json=make_payload("r1", "Acme."))
		self.client.post("/respostas", json=make_payload("r2", "ACME e Zenith."))
		self.client.post("/respostas", json=make_payload("r3", "Nimbus.", "Gemini"))

		response = self.client.get("/share-of-voice?marca=acme")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["percentual"], 66.67)
		platform_results = {
			item["plataforma"]: item for item in response.json()["por_plataforma"]
		}
		self.assertEqual(platform_results["ChatGPT"]["respostas_com_mencao"], 2)
		self.assertEqual(platform_results["Gemini"]["percentual"], 0.0)

	def test_share_of_voice_rejects_unmonitored_brand(self) -> None:
		response = self.client.get("/share-of-voice?marca=Other")

		self.assertEqual(response.status_code, 422)

	def test_top_citations_returns_strongest_mentions_first(self) -> None:
		self.client.post("/respostas", json=make_payload("r2", "Acme."))
		self.client.post("/respostas", json=make_payload("r1", "Acme e Zenith."))
		self.client.post("/respostas", json=make_payload("r3", "Sem marcas."))

		response = self.client.get("/top-citacoes?n=5")

		self.assertEqual(response.status_code, 200)
		self.assertEqual([item["id"] for item in response.json()], ["r1", "r2"])
		self.assertEqual(response.json()[0]["quantidade_marcas"], 2)

	def test_post_validates_and_saves_response(self) -> None:
		response = self.client.post(
			"/respostas",
			json=make_payload("r1", "Acme foi citada."),
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json()["marcas_mencionadas"], ["Acme"])

	def test_post_is_idempotent_and_rejects_conflicting_id(self) -> None:
		payload = make_payload("r1", "Acme foi citada.")
		self.assertEqual(self.client.post("/respostas", json=payload).status_code, 201)

		duplicate_response = self.client.post("/respostas", json=payload)
		conflicting_response = self.client.post(
			"/respostas",
			json=make_payload("r1", "Agora cita Zenith."),
		)

		self.assertEqual(duplicate_response.status_code, 200)
		self.assertFalse(duplicate_response.json()["criada"])
		self.assertEqual(conflicting_response.status_code, 409)

	def test_post_rejects_invalid_payload(self) -> None:
		response = self.client.post("/respostas", json={"id": "r1"})

		self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
	unittest.main()