# Shrinkr — URL Shortener

> Shorten links, share anywhere. Fast. Simple. Reliable.

A full-stack URL shortener built with **FastAPI** and **Vue 3**, featuring real-time click analytics, QR code generation, and link expiry — organized as a clean monorepo.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-shriiinkr.vercel.app-6366F1?style=flat-square&logo=vercel)](https://shriiinkr.vercel.app)
[![API Docs](https://img.shields.io/badge/API%20Docs-shrinkr.up.railway.app%2Fdocs-0B1F3A?style=flat-square&logo=fastapi)](https://shrinkr.up.railway.app/docs)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Vue](https://img.shields.io/badge/Vue-3.x-42b883?style=flat-square&logo=vue.js)](https://vuejs.org)

---

## ✨ Features

- 🔗 **Instant URL Shortening** — Generate short links in milliseconds
- 📊 **Click Analytics** — Track every click with real-time stats
- 📱 **QR Code Generation** — Auto-generate downloadable QR codes for every link
- ⏱️ **Link Expiry** — Set links to expire automatically after hours or days
- 🛡️ **Rate Limiting** — Protected against spam with 10 req/min per IP
- ✏️ **Custom Alias** — Create memorable short links with custom names
- 🔒 **API Key Auth** — Secure endpoints with header-based authentication

---

## 🚀 Live Demo

| Service | URL |
|---|---|
| **Frontend** | [shriiinkr.vercel.app](https://shriiinkr.vercel.app) |
| **API Docs** | [shrinkr.up.railway.app/docs](https://shrinkr.up.railway.app/docs) |

---

## 🛠️ Tech Stack

### Backend
| Tech | Role |
|---|---|
| **FastAPI** | REST API framework |
| **SQLite + SQLAlchemy** | Database & ORM |
| **slowapi** | Rate limiting |
| **qrcode[pil]** | QR code generation |
| **python-dotenv** | Environment variable management |

### Frontend
| Tech | Role |
|---|---|
| **Vue 3** | SPA framework (Composition API + `<script setup>`) |
| **Vite** | Dev server & build tool |
| **Axios** | HTTP client |
| **Lucide Vue** | Icon library |
| **Vue Router 4** | Client-side routing |

---

## 📁 Project Structure

```
shrinkr/
├── backend/                  # FastAPI REST API
│   ├── main.py               # App entry point, routes, middleware
│   ├── database.py           # SQLAlchemy engine & session
│   ├── models.py             # Database models
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── auth.py               # API key authentication
│   ├── Procfile              # Railway deployment config
│   ├── runtime.txt           # Python 3.11 pin
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                  # ← local only, not committed
│
├── frontend/                 # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── api/
│   │   │   └── shortener.js  # Axios API client
│   │   ├── views/
│   │   │   ├── HomeView.vue  # Main page
│   │   │   └── StatsView.vue # Link stats page
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   │   └── favicon.svg
│   ├── package.json
│   ├── vite.config.js
│   └── .env                  # ← local only, not committed
│
└── README.md
```

---

## 🔌 API Reference

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/` | `GET` | ❌ | Health check |
| `/shorten` | `POST` | ✅ | Create a short URL |
| `/urls` | `GET` | ✅ | List all short URLs |
| `/{short_code}` | `GET` | ❌ | Redirect to original URL |
| `/stats/{short_code}` | `GET` | ❌ | View click statistics |
| `/qr/{short_code}` | `GET` | ❌ | Get QR code as PNG |

> **Authentication:** Include `X-API-Key: <your-api-key>` header on protected endpoints.

### Example Request

```bash
curl -X POST https://shrinkr.up.railway.app/shorten \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"long_url": "https://example.com/very/long/url", "custom_alias": "my-link"}'
```

### Example Response

```json
{
  "short_code": "my-link",
  "short_url": "https://shrinkr.up.railway.app/my-link",
  "long_url": "https://example.com/very/long/url",
  "created_at": "2026-07-02T10:00:00"
}
```

---

## ⚙️ Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
# 1. Navigate to backend
cd backend

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
.\venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and set your API_KEY

# 5. Start the server
uvicorn main:app --reload
```

Backend available at:
- **API:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`

### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Set up environment variables
# Create .env with:
# VITE_API_BASE_URL=http://localhost:8000
# VITE_API_KEY=your-api-key-here

# 4. Start the dev server
npm run dev
```

Frontend available at: `http://localhost:5173`

### Running Both Simultaneously

Open two terminals:

```bash
# Terminal 1 — Backend
cd backend && uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend && npm run dev
```

---

## 🚢 Deployment

### Backend → Railway

1. Push to GitHub
2. Create new Railway project → **Deploy from GitHub repo**
3. Set **Root Directory** to `backend`
4. Add environment variables:
   ```
   API_KEY=your-production-api-key
   FRONTEND_URL=https://your-app.vercel.app
   ```
5. Railway auto-detects `Procfile` and `runtime.txt`

### Frontend → Vercel

1. Import repository to Vercel
2. Set **Root Directory** to `frontend`
3. Add environment variables:
   ```
   VITE_API_BASE_URL=https://your-api.railway.app
   VITE_API_KEY=your-production-api-key
   ```
4. Deploy

---

## 🔐 Security

| Measure | Details |
|---|---|
| **API Key Auth** | `POST /shorten` and `GET /urls` require `X-API-Key` header |
| **Rate Limiting** | 10 requests/minute per IP on `/shorten` |
| **SSRF Prevention** | Blocks URLs pointing to localhost or private IP ranges |
| **CORS** | Restricted to configured allowed origins only |
| **SQL Injection** | Prevented by SQLAlchemy ORM (parameterized queries) |

---


## 👤 Author

**Muhammad Khanif Naufal**
- GitHub: [@khanifnaufal](https://github.com/khanifnaufal)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
