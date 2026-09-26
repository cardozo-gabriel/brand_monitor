"""Configuracao do SQLite e SQLAlchemy."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase


DEFAULT_DATABASE_URL = "sqlite:///./brand_monitor.sqlite3"


class Base(DeclarativeBase):
	pass


def create_database_engine(database_url: str = DEFAULT_DATABASE_URL) -> Engine:
	"""Cria uma conexao SQLAlchemy; SQLite pode ser usado entre threads."""
	connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
	return create_engine(database_url, connect_args=connect_args)


def initialize_database(engine: Engine) -> None:
	"""Cria as tabelas do projeto caso ainda nao existam."""
	from app.infrastructure.models import ResponseRecord

	Base.metadata.create_all(bind=engine, tables=[ResponseRecord.__table__])