# URL Shortener API

A simple, fast, and robust URL shortener API built with Python and FastAPI. It features custom alias support, auto-generated short codes, link click analytics, statistics query, and global exception handling.

---

## Tech Stack

This project is built using the following modern Python backend technologies:
*   **FastAPI**: A high-performance Python web framework, easy to use, and automatically provides interactive API documentation (Swagger UI).
*   **SQLite**: A lightweight, serverless relational database for storing URL mappings.
*   **SQLAlchemy**: An Object Relational Mapper (ORM) to interact with the SQLite database securely and efficiently.
*   **Pydantic**: Data validation and settings management using python type annotations.

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

### 4. Run the Local Server (Uvicorn)
Start the FastAPI application with hot-reload enabled:
```bash
uvicorn main:app --reload
```
The application will now be running and accessible at:
*   API Base URL: **`http://127.0.0.1:8000`**
*   Interactive API Docs (Swagger UI): **`http://127.0.0.1:8000/docs`**

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

### 2. Shorten URL
*   **Endpoint**: `POST /shorten`
*   **Description**: Creates a new short URL. If `custom_alias` is not provided, a random 6-character alphanumeric code is automatically generated.
*   **Sample Request Body (JSON)**:
    ```json
    {
      "long_url": "https://google.com",
      "custom_alias": "google"
    }
    ```
*   **Sample Response (201 Created)**:
    ```json
    {
      "short_code": "google",
      "short_url": "http://127.0.0.1:8000/google",
      "long_url": "https://google.com/",
      "created_at": "2026-06-29T15:20:00"
    }
    ```
*   **Possible Errors**:
    *   `400 Bad Request` : If the custom alias is already taken (`"detail": "alias sudah dipakai"`).
    *   `422 Unprocessable Entity` : If the input URL is invalid (e.g. missing HTTP/HTTPS scheme).

### 3. URL Redirection
*   **Endpoint**: `GET /{short_code}`
*   **Description**: Redirects the visitor to the original long URL and increments the click count in the database.
*   **Sample URL**: `http://127.0.0.1:8000/google`
*   **Behavior**: Automatically redirects the client (HTTP Status `307 Temporary Redirect`) to the target long URL (`https://google.com`).
*   **Sample Error (404 Not Found)**:
    ```json
    {
      "detail": "Short URL tidak ditemukan"
    }
    ```

### 4. URL Statistics
*   **Endpoint**: `GET /stats/{short_code}`
*   **Description**: Retrieves the click count and metadata details for a specific short code.
*   **Sample Response (200 OK)**:
    ```json
    {
      "short_code": "google",
      "long_url": "https://google.com/",
      "click_count": 1,
      "created_at": "2026-06-29T15:20:00"
    }
    ```
*   **Sample Error (404 Not Found)**:
    ```json
    {
      "detail": "Short URL tidak ditemukan"
    }
    ```

### 5. List All URLs
*   **Endpoint**: `GET /urls`
*   **Description**: Lists all created short URL records sorted by the newest entry first. Extremely helpful for debugging and demonstration.
*   **Sample Response (200 OK)**:
    ```json
    [
      {
        "short_code": "google",
        "short_url": "http://127.0.0.1:8000/google",
        "long_url": "https://google.com/",
        "click_count": 1,
        "created_at": "2026-06-29T15:20:00"
      },
      {
        "short_code": "YKzcJW",
        "short_url": "http://127.0.0.1:8000/YKzcJW",
        "long_url": "https://google.com/",
        "click_count": 0,
        "created_at": "2026-06-29T15:19:00"
      }
    ]
    ```

---

## Security Considerations

To ensure the safety and reliability of the service, several security measures have been implemented:
*   **Rate Limiting**: Integrated `slowapi` to prevent API abuse and brute-force attempts. The `POST /shorten` endpoint is limited to **10 requests per minute per IP address**. Exceeding this limit returns an HTTP `429 Too Many Requests` error.
*   **Internal Network Scanning (SSRF) Prevention**: The API validates the `long_url` before shortening it. Any target URL resolving to localhost (`127.0.0.1`, `::1`), private IP ranges (e.g., `10.x.x.x`, `192.168.x.x`), or link-local addresses is blocked (returning HTTP `400 Bad Request`).
*   **Redirect Loop Prevention**: The API prevents users from shortening a URL that points to an existing short code on the same server, eliminating circular redirections.
*   **SQL Injection Protection**: Database queries are built using SQLAlchemy's ORM, which automatically uses parameterized queries to secure inputs against SQL injection.

---

## Future Improvements

Planned features for future iterations:
1.  **Expiry Link**: Add expiration timestamps to short links (e.g. link expires in 24 hours or 7 days).
2.  **Malicious URL Screening**: Integrate the Google Safe Browsing API to automatically screen and block malicious or phishing URLs.
3.  **API Key Authentication**: Require an API key for the `/shorten` endpoint to control access and assign custom quotas.
4.  **Custom Domain**: Support unique custom domain names as the base of the generated short URLs.
5.  **User Authentication**: Implement user registration and login so users can manage (edit/delete) their own links.
