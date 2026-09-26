"""Configuracao do SQLite e SQLAlchemy."""

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session

from app.domain.schemas import normalize_platform_name


DEFAULT_DATABASE_URL = "sqlite:///./brand_monitor.sqlite3"


class Base(DeclarativeBase):
	pass


def create_database_engine(database_url: str = DEFAULT_DATABASE_URL) -> Engine:
	"""Cria uma conexao SQLAlchemy; SQLite pode ser usado entre threads."""
	connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
	return create_engine(database_url, connect_args=connect_args)


def initialize_database(engine: Engine) -> None:
	"""Cria as tabelas e consolida aliases ja persistidos de plataformas."""
	from app.infrastructure.models import ResponseRecord

	Base.metadata.create_all(bind=engine, tables=[ResponseRecord.__table__])
	with Session(engine) as session:
		records = session.scalars(select(ResponseRecord)).all()
		updated = False
		for record in records:
			platform = normalize_platform_name(record.plataforma)
			if platform != record.plataforma:
				record.plataforma = platform
				updated = True
		if updated:
			session.commit()