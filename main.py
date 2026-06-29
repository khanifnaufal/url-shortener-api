from fastapi import FastAPI

import models
from database import Base, engine

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
