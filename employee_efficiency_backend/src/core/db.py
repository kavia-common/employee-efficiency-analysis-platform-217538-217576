import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
from dotenv import load_dotenv

load_dotenv()

# PUBLIC_INTERFACE
def get_database_url() -> str:
    """Return the DATABASE_URL from env, defaulting to local Postgres at port 5001."""
    return os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5001/employee_efficiency")


class Base(DeclarativeBase):
    """Base for SQLAlchemy models."""
    pass


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# PUBLIC_INTERFACE
def get_db() -> Generator:
    """Provide a SQLAlchemy session dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PUBLIC_INTERFACE
def init_db() -> None:
    """Create all tables if they do not exist."""
    # Import models for side effects so metadata is populated.
    from src.core import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
