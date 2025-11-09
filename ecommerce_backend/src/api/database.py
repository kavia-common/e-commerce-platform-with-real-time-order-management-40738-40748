from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from .config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class."""
    pass


settings = get_settings()

# Create engine; for SQLite enable check_same_thread
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
