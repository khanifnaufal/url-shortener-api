# Shrinkr — URL Shortener Monorepo

A full-stack URL shortener with a **FastAPI** backend and a **Vue 3** frontend, organized as a monorepo.

## 🚀 Live Demo

| Service | Link |
|---|---|
| **Frontend** | [shrinkr.vercel.app](https://shrinkr.vercel.app) *(placeholder — update after deploy)* |
| **API Docs** | [shrinkr-api.railway.app/docs](https://shrinkr-api.railway.app/docs) *(placeholder — update after deploy)* |

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
│   ├── Procfile          # Railway deployment
│   ├── runtime.txt       # Python 3.11
│   ├── requirements.txt
│   ├── .env              # ← local only, not committed
│   └── .env.example
│
├── frontend/         # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── api/
│   │   │   └── shortener.js   # Axios API client
│   │   ├── views/
│   │   │   ├── HomeView.vue   # Main page
│   │   │   └── StatsView.vue  # URL stats page
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   │   └── favicon.svg
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
| **Lucide Vue** | Icon library |

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
| `/shorten` | POST | ✅ Required | Buat short URL |
| `/urls` | GET | ✅ Required | List semua URL |
| `/{short_code}` | GET | ❌ | Redirect ke long URL |
| `/stats/{short_code}` | GET | ❌ | Lihat statistik klik |
| `/qr/{short_code}` | GET | ❌ | QR code PNG |

> **Auth**: Kirim header `X-API-Key: <your-api-key>` pada endpoint yang memerlukan autentikasi.

---

## Deployment

### Backend — Railway

1. Push ke GitHub
2. Create new Railway project → Deploy from GitHub
3. Set environment variables:
   ```
   API_KEY=your-production-api-key
   FRONTEND_URL=https://your-app.vercel.app
   ```
4. Railway otomatis deteksi `Procfile` dan `runtime.txt`

### Frontend — Vercel

1. Import repository ke Vercel
2. Set **Root Directory** ke `frontend`
3. Set environment variables:
   ```
   VITE_API_BASE_URL=https://your-api.railway.app
   VITE_API_KEY=your-production-api-key
   ```

---

## Security

- **API Key Authentication** — `POST /shorten` dan `GET /urls` dilindungi `X-API-Key` header
- **Rate Limiting** — `POST /shorten` dibatasi 10 request/menit per IP
- **SSRF Prevention** — URL yang mengarah ke localhost/IP privat diblokir
- **CORS** — Hanya origin yang diizinkan yang bisa akses backend

---

## Future Improvements

* **Malicious URL Screening** — Integrasi Google Safe Browsing API untuk memblokir link berbahaya
* **Custom Domain** — Support domain kustom sebagai base URL untuk short link
* **User Authentication** — Login untuk manajemen link pribadi dan dashboard personal
* **Bulk Shorten** — Mempersingkat banyak URL sekaligus dalam satu request
* **Frontend Dashboard** — UI lengkap untuk manage dan monitor semua short URL dengan filter dan export
