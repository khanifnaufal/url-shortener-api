# URL Shortener API

A simple, fast, and robust URL shortener API built with Python and FastAPI. It features custom alias support, auto-generated short codes, link expiration, QR code generation, API key authentication, click analytics, and global exception handling.

---

## Tech Stack

This project is built using the following modern Python backend technologies:
*   **FastAPI**: A high-performance Python web framework, easy to use, and automatically provides interactive API documentation (Swagger UI).
*   **SQLite**: A lightweight, serverless relational database for storing URL mappings.
*   **SQLAlchemy**: An Object Relational Mapper (ORM) to interact with the SQLite database securely and efficiently.
*   **Pydantic**: Data validation and settings management using python type annotations.
*   **slowapi**: Rate limiting middleware for FastAPI.
*   **qrcode[pil]**: QR code image generation library.
*   **python-dotenv**: Loads environment variables from `.env` file.

---

## Installation & Getting Started

Follow the steps below to run this project on your local machine:

### 1. Clone the Repository
Download the project files to your local machine:
```bash
git clone https://github.com/khanifnaufal/url-shortener-api.git
cd url-shortener-api
```

### 2. Create & Activate a Virtual Environment (Recommended)
Isolate your project dependencies by setting up a virtual environment:

*   **Windows (PowerShell/CMD):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   **macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file and fill in your secret API key:
```bash
cp .env.example .env
```
Then edit `.env`:
```
API_KEY=your-secret-api-key-here
```
> ⚠️ **Never commit `.env` to version control.** It is already listed in `.gitignore`.

### 5. Run the Local Server (Uvicorn)
Start the FastAPI application with hot-reload enabled:
```bash
uvicorn main:app --reload
```
The application will now be running and accessible at:
*   API Base URL: **`http://127.0.0.1:8000`**
*   Interactive API Docs (Swagger UI): **`http://127.0.0.1:8000/docs`**

---

## Authentication

Some endpoints require an **API key** to be passed via the `X-API-Key` HTTP header.

### Which endpoints require authentication?
| Endpoint | Auth Required |
|---|---|
| `POST /shorten` | ✅ Yes |
| `GET /urls` | ✅ Yes |
| `GET /{short_code}` | ❌ No (public redirect) |
| `GET /stats/{short_code}` | ❌ No (public stats) |
| `GET /qr/{short_code}` | ❌ No (public QR code) |

### How to use in Postman
1. Open Postman and select your request (e.g., `POST /shorten`).
2. Go to the **Headers** tab.
3. Add a new key: `X-API-Key` with value: `your-secret-api-key-here`.
4. Send the request.

### Example using curl
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{"long_url": "https://google.com"}'
```

### Error Responses
*   **`401 Unauthorized`** — Header `X-API-Key` tidak ada atau nilainya salah:
    ```json
    { "detail": "API key tidak valid atau tidak ditemukan" }
    ```
*   **`422 Unprocessable Entity`** — Header `X-API-Key` tidak dikirim sama sekali (FastAPI validation).

---

## API Endpoints

### 1. Health Check
*   **Endpoint**: `GET /`
*   **Description**: Checks if the API is running correctly.
*   **Sample Response (200 OK)**:
    ```json
    {
      "message": "URL Shortener API is running"
    }
    ```

### 2. Shorten URL 🔒
*   **Endpoint**: `POST /shorten`
*   **Auth**: Required (`X-API-Key` header)
*   **Description**: Creates a new short URL. Optionally set a custom alias and/or expiry duration.
*   **Sample Request Body (JSON)**:
    ```json
    {
      "long_url": "https://google.com",
      "custom_alias": "google",
      "expires_in_hours": 24
    }
    ```
*   **Sample Response (201 Created)**:
    ```json
    {
      "short_code": "google",
      "short_url": "http://127.0.0.1:8000/google",
      "long_url": "https://google.com/",
      "created_at": "2026-07-01T12:00:00",
      "expires_at": "2026-07-02T12:00:00"
    }
    ```
*   **Possible Errors**:
    *   `400 Bad Request`: Custom alias already taken.
    *   `401 Unauthorized`: Missing or invalid API key.
    *   `422 Unprocessable Entity`: Invalid URL or input.

### 3. URL Redirection
*   **Endpoint**: `GET /{short_code}`
*   **Description**: Redirects the visitor to the original long URL and increments the click count.
*   **Sample URL**: `http://127.0.0.1:8000/google`
*   **Behavior**: Redirects (HTTP `307`) to the target long URL.
*   **Possible Errors**:
    *   `404 Not Found`: Short code does not exist.
    *   `410 Gone`: Short URL has expired.

### 4. URL Statistics
*   **Endpoint**: `GET /stats/{short_code}`
*   **Description**: Retrieves click count and metadata for a specific short code.
*   **Sample Response (200 OK)**:
    ```json
    {
      "short_code": "google",
      "long_url": "https://google.com/",
      "click_count": 5,
      "created_at": "2026-07-01T12:00:00",
      "expires_at": "2026-07-02T12:00:00",
      "is_expired": false,
      "qr_url": "/qr/google"
    }
    ```

### 5. List All URLs 🔒
*   **Endpoint**: `GET /urls`
*   **Auth**: Required (`X-API-Key` header)
*   **Description**: Lists all created short URL records sorted by newest first.

### 6. QR Code
*   **Endpoint**: `GET /qr/{short_code}`
*   **Description**: Returns a QR code PNG image for the given short code. Generated on-the-fly in memory.
*   **Sample URL**: `http://127.0.0.1:8000/qr/google`
*   **Response**: `image/png` — open directly in a browser to display.

---

## Security Considerations

*   **API Key Authentication**: `POST /shorten` and `GET /urls` are protected by an `X-API-Key` header. The key is stored in `.env` and never committed to version control. Comparison uses `secrets.compare_digest` to prevent timing attacks.
*   **Rate Limiting**: Integrated `slowapi` to prevent API abuse. The `POST /shorten` endpoint is limited to **10 requests per minute per IP**. Returns `429 Too Many Requests` when exceeded.
*   **SSRF Prevention**: Any `long_url` resolving to localhost, private IP ranges, or link-local addresses is blocked (`400 Bad Request`).
*   **Redirect Loop Prevention**: Shortening a URL that points to an existing short code on the same server is blocked.
*   **SQL Injection Protection**: All queries use SQLAlchemy ORM with parameterized statements.

---

## Future Improvements

Planned features for future iterations:
1.  **Malicious URL Screening**: Integrate Google Safe Browsing API to block phishing URLs.
2.  **Custom Domain**: Support custom domain names as the base of generated short URLs.
3.  **User Authentication**: User registration and login so users can manage their own links.
4.  **Bulk Shorten**: Accept multiple URLs in a single `POST /shorten` request.
