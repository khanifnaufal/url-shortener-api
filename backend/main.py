from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse, StreamingResponse
import io
import qrcode
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import string
import secrets
import logging
import os
from typing import List
from urllib.parse import urlparse
import socket
import ipaddress
from datetime import datetime, timedelta, timezone

# Slowapi imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import models
from database import Base, engine, get_db
from schemas import ShortenRequest, ShortenResponse, URLStatsResponse, URLDetailResponse
from auth import verify_api_key

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup slowapi Limiter
limiter = Limiter(key_func=get_remote_address)

# Buat semua tabel di database saat aplikasi pertama kali dijalankan.
# Jika tabel sudah ada, perintah ini diabaikan (tidak menghapus data).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="API untuk memperpendek URL panjang menjadi short code yang mudah dibagikan.",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — izinkan frontend Vue (Vite dev server) mengakses API
allowed_origins = [
    "http://localhost:5173",
    "https://url-shortener-api-gilt.vercel.app",
    "https://*.vercel.app",
    os.getenv("FRONTEND_URL", ""),
]
# Filter out empty strings
allowed_origins = [o for o in allowed_origins if o]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_private_or_local_url(url: str) -> bool:
    """Mengecek apakah URL mengarah ke localhost, loopback, link-local, atau range IP privat."""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return True

        # Cek host lokal secara langsung
        if hostname.lower() in ("localhost", "127.0.0.1", "[::1]", "0.0.0.0"):
            return True

        # Cek apakah hostname adalah IP Address dan periksa range-nya
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_loopback or ip.is_private or ip.is_link_local:
                return True
        except ValueError:
            # Jika bukan IP Address langsung, coba resolve via DNS
            try:
                ip_str = socket.gethostbyname(hostname)
                ip = ipaddress.ip_address(ip_str)
                if ip.is_loopback or ip.is_private or ip.is_link_local:
                    return True
            except Exception:
                pass

        return False
    except Exception:
        return True


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    # Jika exception adalah RateLimitExceeded dari slowapi
    if isinstance(exc, RateLimitExceeded):
        return _rate_limit_exceeded_handler(request, exc)

    # Jika exception adalah HTTPException, kembalikan detail aslinya
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    # Jika exception adalah validation error dari Pydantic/FastAPI, kembalikan detail validasinya
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()}
        )

    # Log stack trace di sisi server
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Kembalikan error 500 bersih ke user
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Terjadi kesalahan internal pada server. Silakan coba beberapa saat lagi."}
    )


@app.get("/", tags=["Health Check"])
def root():
    """Endpoint health check — memastikan API berjalan dengan baik."""
    return {"message": "URL Shortener API is running"}


@app.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED, tags=["URL Shortener"], dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
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
    # A. Cek apakah long_url mengarah ke localhost atau IP privat (mencegah SSRF/network scanning)
    if is_private_or_local_url(str(payload.long_url)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL tidak diperbolehkan (localhost atau IP privat)"
        )

    # B. Cek apakah long_url mengarah ke short_code dari domain sendiri (mencegah loop redireksi)
    parsed_long = urlparse(str(payload.long_url))
    request_host = request.url.netloc

    if parsed_long.netloc == request_host:
        path_parts = [p for p in parsed_long.path.split("/") if p]
        if path_parts:
            short_code_candidate = path_parts[0]
            existing_short = db.query(models.URL).filter(models.URL.short_code == short_code_candidate).first()
            if existing_short:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="URL tidak diperbolehkan karena dapat menyebabkan loop redireksi"
                )

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

    # 2. Hitung expires_at jika expires_in_hours diisi
    expires_at = None
    if payload.expires_in_hours is not None:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=payload.expires_in_hours)

    # 3. Simpan ke database
    db_url = models.URL(
        short_code=short_code,
        long_url=str(payload.long_url),
        expires_at=expires_at
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # 4. Buat short_url lengkap menggunakan base_url dari request
    short_url = f"{request.base_url}{db_url.short_code}"

    return ShortenResponse(
        short_code=db_url.short_code,
        short_url=short_url,
        long_url=db_url.long_url,
        created_at=db_url.created_at,
        expires_at=db_url.expires_at
    )


@app.get("/urls", response_model=List[URLDetailResponse], tags=["URL Stats"], dependencies=[Depends(verify_api_key)])
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


@app.get("/qr/{short_code}", tags=["QR Code"])
def get_qr_code(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Generate dan kembalikan QR code PNG untuk short_code tertentu.

    QR code berisi full short URL (misal: http://localhost:8000/{short_code}).
    Gambar dibuat on-the-fly di memory, tidak disimpan ke disk.
    """
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL tidak ditemukan"
        )

    # Buat full short URL yang akan dikodekan ke dalam QR code
    short_url = f"{request.base_url}{short_code}"

    # Generate QR code di memory menggunakan BytesIO (tanpa menyimpan ke disk)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.get("/stats/{short_code}", response_model=URLStatsResponse, tags=["URL Stats"])
def get_url_stats(
    short_code: str,
    db: Session = Depends(get_db)
):
    """
    Mendapatkan statistik akses (click_count) untuk short_code tertentu.
    Menyertakan qr_url — link ke endpoint QR code untuk short_code ini.
    """
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL tidak ditemukan"
        )

    return URLStatsResponse(
        short_code=db_url.short_code,
        long_url=db_url.long_url,
        click_count=db_url.click_count,
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
        is_expired=(
            db_url.expires_at is not None
            and datetime.now(timezone.utc) > db_url.expires_at.replace(tzinfo=timezone.utc)
            if db_url.expires_at and db_url.expires_at.tzinfo is None
            else (
                db_url.expires_at is not None
                and datetime.now(timezone.utc) > db_url.expires_at
            )
        ),
        qr_url=f"/qr/{db_url.short_code}"
    )


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

    # Cek apakah link sudah expired
    if db_url.expires_at is not None:
        # Handle expires_at yang mungkin naive (tanpa timezone info) dari SQLite
        expires_at = db_url.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Short URL ini sudah expired"
            )

    # Increment click_count
    db_url.click_count += 1
    db.commit()

    # Redirect ke long_url dengan status code 307
    return RedirectResponse(url=db_url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

