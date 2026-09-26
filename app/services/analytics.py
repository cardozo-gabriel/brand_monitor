"""Metricas de share of voice e ranking de citacoes."""

from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any

from app.services.brand_detector import MONITORED_BRANDS, detect_brands


def normalize_brand_name(brand: str) -> str:
	for monitored_brand in MONITORED_BRANDS:
		if monitored_brand.casefold() == brand.strip().casefold():
			return monitored_brand
	raise ValueError(f"Marca nao monitorada: {brand}.")


def _percentage(mentions: int, total: int) -> float:
	return round(mentions * 100 / total, 2) if total else 0.0


def calculate_share_of_voice(
	responses: Iterable[Mapping[str, Any]],
	brand: str,
) -> dict[str, Any]:
	canonical_brand = normalize_brand_name(brand)
	total_responses = 0
	mention_count = 0
	platform_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])

	for response in responses:
		total_responses += 1
		mentioned_brands = detect_brands(response["resposta_texto"])
		is_mentioned = canonical_brand in mentioned_brands
		mention_count += int(is_mentioned)

		platform = response["plataforma"]
		platform_counts[platform][0] += 1
		platform_counts[platform][1] += int(is_mentioned)

	return {
		"marca": canonical_brand,
		"total_respostas": total_responses,
		"respostas_com_mencao": mention_count,
		"percentual": _percentage(mention_count, total_responses),
		"por_plataforma": [
			{
				"plataforma": platform,
				"total_respostas": counts[0],
				"respostas_com_mencao": counts[1],
				"percentual": _percentage(counts[1], counts[0]),
			}
			for platform, counts in sorted(platform_counts.items())
		],
	}


def rank_top_citations(
	responses: Iterable[Mapping[str, Any]],
	limit: int,
) -> list[dict[str, Any]]:
	ranked_responses = []
	for response in responses:
		mentioned_brands = detect_brands(response["resposta_texto"])
		if not mentioned_brands:
			continue

		ranked_responses.append(
			{
				**response,
				"marcas_mencionadas": mentioned_brands,
				"quantidade_marcas": len(mentioned_brands),
			}
		)

	ranked_responses.sort(
		key=lambda response: (-response["quantidade_marcas"], response["id"])
	)
	return ranked_responses[:limit]
