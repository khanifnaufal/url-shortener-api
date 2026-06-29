from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import string
import secrets

import models
from database import Base, engine, get_db
from typing import List
from schemas import ShortenRequest, ShortenResponse, URLStatsResponse, URLDetailResponse

# Buat semua tabel di database saat aplikasi pertama kali dijalankan.
# Jika tabel sudah ada, perintah ini diabaikan (tidak menghapus data).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="API untuk memperpendek URL panjang menjadi short code yang mudah dibagikan.",
    version="1.0.0",
)


@app.get("/", tags=["Health Check"])
def root():
    """Endpoint health check — memastikan API berjalan dengan baik."""
    return {"message": "URL Shortener API is running"}


@app.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED, tags=["URL Shortener"])
def shorten_url(
    payload: ShortenRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk memperpendek URL panjang.

    Menerima URL panjang dan alias opsional. Menghasilkan short code unik,
    menyimpan ke database, dan mengembalikan respon berupa short code dan URL pendek.
    """
    # 1. Tentukan short_code yang akan digunakan
    if payload.custom_alias:
        short_code = payload.custom_alias
        # Cek apakah alias sudah digunakan
        existing_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if existing_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="alias sudah dipakai"
            )
    else:
        # Generate random short_code 6 karakter alphanumeric
        # Retry generate kalau ternyata sudah ada di database (max 5x retry)
        characters = string.ascii_letters + string.digits
        max_retries = 5
        short_code = None

        for _ in range(max_retries):
            potential_code = "".join(secrets.choice(characters) for _ in range(6))
            existing_url = db.query(models.URL).filter(models.URL.short_code == potential_code).first()
            if not existing_url:
                short_code = potential_code
                break

        if not short_code:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gagal menghasilkan short code unik setelah 5 kali percobaan."
            )

    # 2. Simpan ke database
    db_url = models.URL(
        short_code=short_code,
        long_url=str(payload.long_url)
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # 3. Buat short_url lengkap menggunakan base_url dari request
    short_url = f"{request.base_url}{db_url.short_code}"

    return ShortenResponse(
        short_code=db_url.short_code,
        short_url=short_url,
        long_url=db_url.long_url,
        created_at=db_url.created_at
    )


@app.get("/urls", response_model=List[URLDetailResponse], tags=["URL Stats"])
def list_urls(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Melihat semua short URL yang pernah dibuat, diurutkan dari yang terbaru.
    """
    db_urls = db.query(models.URL).order_by(models.URL.created_at.desc(), models.URL.id.desc()).all()

    # Buat response list yang menyertakan short_url dinamis
    response_list = []
    for db_url in db_urls:
        response_list.append(
            URLDetailResponse(
                short_code=db_url.short_code,
                short_url=f"{request.base_url}{db_url.short_code}",
                long_url=db_url.long_url,
                click_count=db_url.click_count,
                created_at=db_url.created_at
            )
        )
    return response_list


@app.get("/stats/{short_code}", response_model=URLStatsResponse, tags=["URL Stats"])
def get_url_stats(
    short_code: str,
    db: Session = Depends(get_db)
):
    """
    Mendapatkan statistik akses (click_count) untuk short_code tertentu.
    """
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL tidak ditemukan"
        )
    return db_url


@app.get("/{short_code}", tags=["URL Shortener"])
def redirect_to_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    """
    Redirect short code ke original URL dan menambahkan jumlah klik (click_count).
    """
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL tidak ditemukan"
        )

    # Increment click_count
    db_url.click_count += 1
    db.commit()

    # Redirect ke long_url dengan status code 307
    return RedirectResponse(url=db_url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

