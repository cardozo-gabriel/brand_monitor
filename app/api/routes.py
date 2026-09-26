"""Endpoints HTTP."""

from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from app.domain.schemas import ResponseSchema
from app.infrastructure.repositories import ResponseRepository
from app.services.analytics import calculate_share_of_voice, rank_top_citations
from app.services.brand_detector import detect_brands

router = APIRouter()


def get_session(request: Request) -> Iterator[Session]:
	with Session(request.app.state.engine) as session:
		yield session


@router.get("/share-of-voice")
def share_of_voice(
	marca: str = Query(min_length=1),
	session: Session = Depends(get_session),
) -> dict[str, object]:
	responses = [record.to_dict() for record in ResponseRepository(session).list_all()]
	try:
		return calculate_share_of_voice(responses, marca)
	except ValueError as error:
		raise HTTPException(status_code=422, detail=str(error)) from error


@router.get("/top-citacoes")
def top_citations(
	n: int = Query(default=5, ge=1, le=100),
	session: Session = Depends(get_session),
) -> list[dict[str, object]]:
	responses = [record.to_dict() for record in ResponseRepository(session).list_all()]
	return rank_top_citations(responses, n)


@router.post("/respostas", status_code=201)
def create_response(
	payload: ResponseSchema,
	response: Response,
	session: Session = Depends(get_session),
) -> dict[str, object]:
	response_data = payload.model_dump(mode="json")
	try:
		inserted_count, _ = ResponseRepository(session).save_many([response_data])
	except ValueError as error:
		raise HTTPException(status_code=409, detail=str(error)) from error

	response.status_code = 201 if inserted_count else 200
	return {
		"id": payload.id,
		"criada": bool(inserted_count),
		"marcas_mencionadas": detect_brands(payload.resposta_texto),
	}
