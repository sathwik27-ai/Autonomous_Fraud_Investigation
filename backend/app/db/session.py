from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings
from .models import Base

db_url = settings.sqlalchemy_database_url
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db():
    """Ensure database tables exist on startup for both SQLite and PostgreSQL.
    In Postgres, running Base.metadata.create_all(engine) creates tables if missing,
    ensuring newly connected cloud databases (Render/Neon/Supabase) work out-of-the-box."""
    try:
        Base.metadata.create_all(engine)
    except Exception as exc:
        print(f"[db] init_db note: {exc}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
