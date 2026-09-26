"""Testes para deteccao de marcas."""

import unittest

from app.services.brand_detector import detect_brands


class DetectBrandsTests(unittest.TestCase):
	def test_detects_all_monitored_brands_without_case_sensitivity(self) -> None:
		result = detect_brands("ACME, zenith e NIMBUS aparecem nesta resposta.")

		self.assertEqual(result, ["Acme", "Zenith", "Nimbus"])

	def test_detects_dotted_acme_spelling(self) -> None:
		self.assertEqual(detect_brands("A A.C.M.E. foi citada."), ["Acme"])

	def test_returns_a_brand_only_once(self) -> None:
		self.assertEqual(detect_brands("Acme e ACME; Acme novamente."), ["Acme"])

	def test_does_not_match_brands_inside_other_words(self) -> None:
		text = "Acmeish, xZenith, Nimbus_Pro e Zenith2 nao sao citacoes isoladas."

		self.assertEqual(detect_brands(text), [])

	def test_returns_no_brands_for_empty_or_unrelated_text(self) -> None:
		self.assertEqual(detect_brands(""), [])
		self.assertEqual(detect_brands("Sem marcas monitoradas."), [])

	def test_rejects_non_text_input(self) -> None:
		with self.assertRaisesRegex(TypeError, "precisa ser uma string"):
			detect_brands(None)  # type: ignore[arg-type]


if __name__ == "__main__":
	unittest.main()