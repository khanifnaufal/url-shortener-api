import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status
import secrets

# Load variabel dari file .env (jika ada)
load_dotenv()

# Baca API_KEY dari environment variable saat module pertama kali di-import
_API_KEY = os.getenv("API_KEY")

if not _API_KEY:
    raise RuntimeError(
        "API_KEY environment variable belum di-set. "
        "Buat file .env dan isi dengan API_KEY=<your-secret-key>, "
        "atau set environment variable secara langsung sebelum menjalankan server."
    )


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    FastAPI dependency untuk verifikasi API key dari header X-API-Key.

    Gunakan sebagai dependency di endpoint yang memerlukan autentikasi:
        @app.post("/shorten", dependencies=[Depends(verify_api_key)])

    Raises:
        HTTPException 401: Jika header X-API-Key tidak ada atau nilainya salah.
    """
    # Gunakan secrets.compare_digest untuk mencegah timing attack
    if not secrets.compare_digest(x_api_key, _API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key tidak valid atau tidak ditemukan",
            headers={"WWW-Authenticate": "ApiKey"},
        )
