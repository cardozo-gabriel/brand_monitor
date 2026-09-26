"""Testes para metricas e ranking de citacoes."""

import unittest

from app.services.analytics import calculate_share_of_voice, rank_top_citations


def make_response(response_id: str, platform: str, text: str) -> dict[str, str]:
	return {
		"id": response_id,
		"plataforma": platform,
		"resposta_texto": text,
	}


class AnalyticsTests(unittest.TestCase):
	def test_calculates_overall_and_per_platform_share(self) -> None:
		responses = [
			make_response("r1", "ChatGPT", "Acme e Zenith."),
			make_response("r2", "ChatGPT", "ACME."),
			make_response("r3", "Gemini", "Nimbus."),
		]

		result = calculate_share_of_voice(responses, "acme")

		self.assertEqual(result["marca"], "Acme")
		self.assertEqual(result["total_respostas"], 3)
		self.assertEqual(result["respostas_com_mencao"], 2)
		self.assertEqual(result["percentual"], 66.67)
		platform_results = {
			item["plataforma"]: item for item in result["por_plataforma"]
		}
		self.assertEqual(platform_results["ChatGPT"]["percentual"], 100.0)
		self.assertEqual(platform_results["Gemini"]["percentual"], 0.0)

	def test_empty_dataset_has_zero_share(self) -> None:
		result = calculate_share_of_voice([], "Nimbus")

		self.assertEqual(result["percentual"], 0.0)
		self.assertEqual(result["por_plataforma"], [])

	def test_rejects_unmonitored_brand(self) -> None:
		with self.assertRaisesRegex(ValueError, "Marca nao monitorada"):
			calculate_share_of_voice([], "Other")

	def test_ranks_by_distinct_brand_count_and_uses_id_for_ties(self) -> None:
		responses = [
			make_response("r3", "Gemini", "Nimbus."),
			make_response("r2", "ChatGPT", "Acme."),
			make_response("r1", "ChatGPT", "Acme e Zenith, Acme."),
			make_response("r4", "Gemini", "Sem marcas."),
		]

		result = rank_top_citations(responses, 3)

		self.assertEqual([item["id"] for item in result], ["r1", "r2", "r3"])
		self.assertEqual(result[0]["marcas_mencionadas"], ["Acme", "Zenith"])
		self.assertEqual(result[0]["quantidade_marcas"], 2)


if __name__ == "__main__":
	unittest.main()
