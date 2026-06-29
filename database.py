from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL koneksi ke SQLite — file shortener.db akan dibuat otomatis di folder project
DATABASE_URL = "sqlite:///./shortener.db"

# Engine SQLAlchemy
# connect_args={"check_same_thread": False} diperlukan khusus untuk SQLite
# agar bisa dipakai di multi-thread (FastAPI berjalan async)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Session factory — setiap request FastAPI akan membuat satu session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class untuk semua model SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Dependency injection FastAPI untuk mendapatkan sesi database.

    Cara pakai di endpoint:
        from database import get_db
        from sqlalchemy.orm import Session
        from fastapi import Depends

        @app.get("/contoh")
        def contoh(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
