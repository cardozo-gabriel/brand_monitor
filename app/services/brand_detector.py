"""Deteccao de marcas baseada em expressoes regulares."""

import re


MONITORED_BRANDS = ("Acme", "Zenith", "Nimbus")

BRAND_PATTERNS = {
	"Acme": re.compile(r"(?<!\w)a\.?c\.?m\.?e\.?(?!\w)", re.IGNORECASE),
	"Zenith": re.compile(r"(?<!\w)zenith(?!\w)", re.IGNORECASE),
	"Nimbus": re.compile(r"(?<!\w)nimbus(?!\w)", re.IGNORECASE),
}


def detect_brands(text: str) -> list[str]:
	"""Retorna cada marca monitorada encontrada no texto, uma unica vez."""
	if not isinstance(text, str):
		raise TypeError("O texto da resposta precisa ser uma string.")

	return [
		brand
		for brand in MONITORED_BRANDS
		if BRAND_PATTERNS[brand].search(text)
	]