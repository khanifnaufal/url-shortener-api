# URL Shortener — Monorepo

A full-stack URL shortener with a **FastAPI** backend and a **Vue 3** frontend, organized as a monorepo.

---

## Project Structure

```
url-shortener-api/
├── backend/          # FastAPI REST API
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── requirements.txt
│   ├── .env              # ← local only, not committed
│   └── .env.example
│
├── frontend/         # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── api/
│   │   │   └── shortener.js   # Axios API client
│   │   ├── components/
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env              # ← local only, not committed
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore        # Root gitignore (covers both backend & frontend)
└── README.md
```

---

## Tech Stack

### Backend
| Tech | Role |
|---|---|
| **FastAPI** | REST API framework |
| **SQLite + SQLAlchemy** | Database & ORM |
| **slowapi** | Rate limiting |
| **qrcode[pil]** | QR code generation |
| **python-dotenv** | Environment variables |

### Frontend
| Tech | Role |
|---|---|
| **Vue 3** | SPA framework (Composition API) |
| **Vite** | Dev server & build tool |
| **Axios** | HTTP client for API calls |

---

## Getting Started

### Backend

#### 1. Masuk ke folder backend
```bash
cd backend
```

#### 2. Buat & aktifkan virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup environment variables
```bash
cp .env.example .env
```
Edit `.env`:
```
API_KEY=your-secret-api-key-here
```

#### 5. Jalankan server
```bash
uvicorn main:app --reload
```

Backend berjalan di:
- **API**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`

---

### Frontend

#### 1. Masuk ke folder frontend
```bash
cd frontend
```

#### 2. Install dependencies
```bash
npm install
```

#### 3. Setup environment variables
```bash
# Edit .env yang sudah ada, atau buat baru:
```
Isi `.env`:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_API_KEY=your-secret-api-key-here   # sama dengan API_KEY di backend/.env
```

#### 4. Jalankan dev server
```bash
npm run dev
```

Frontend berjalan di: **`http://localhost:5173`**

---

## Running Both Simultaneously

Buka **dua terminal terpisah**:

**Terminal 1 — Backend:**
```bash
cd backend
.\venv\Scripts\activate   # Windows
uvicorn main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

---

## API Overview

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/` | GET | ❌ | Health check |
| `/shorten` | POST | ✅ | Buat short URL |
| `/urls` | GET | ✅ | List semua URL |
| `/{short_code}` | GET | ❌ | Redirect ke long URL |
| `/stats/{short_code}` | GET | ❌ | Lihat statistik klik |
| `/qr/{short_code}` | GET | ❌ | QR code PNG |

> **Auth**: Kirim header `X-API-Key: <your-api-key>` pada endpoint yang memerlukan autentikasi.

---

## Security

- **API Key Authentication** — `POST /shorten` dan `GET /urls` dilindungi `X-API-Key` header
- **Rate Limiting** — `POST /shorten` dibatasi 10 request/menit per IP
- **SSRF Prevention** — URL yang mengarah ke localhost/IP privat diblokir
- **CORS** — Frontend di `http://localhost:5173` diizinkan akses backend

---

## Future Improvements

1. **Malicious URL Screening** — Integrasi Google Safe Browsing API
2. **Custom Domain** — Support domain kustom sebagai base URL
3. **User Authentication** — Login untuk manajemen link pribadi
4. **Bulk Shorten** — Mempendekkan banyak URL dalam satu request
5. **Frontend Dashboard** — UI lengkap untuk manage dan monitor semua short URL
