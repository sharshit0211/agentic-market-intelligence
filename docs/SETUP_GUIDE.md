# Setup & Deployment Guide — MarketIntel AI

This guide provides step-by-step instructions for running the MarketIntel AI platform locally in development mode.

---

## 1. Prerequisites

Verify you have installed:
- **Node.js**: v18.0.0 or higher (`node -v`)
- **npm**: v9.0.0 or higher (`npm -v`)
- **Python**: v3.11 or higher (`python --version`)
- **PostgreSQL**: v15 or higher (Optional for running Phase 1 foundation; required for persistent database operations)

---

## 2. Environment Configuration

Copy `.env.example` in the project root to `.env`:
```bash
cp .env.example .env
```

Key environment parameters:
- `BACKEND_PORT`: Port on which FastAPI listens (default: `8000`).
- `NEXT_PUBLIC_API_URL`: Base API URL consumed by Next.js (default: `http://localhost:8000/api/v1`).
- `DATABASE_URL`: PostgreSQL connection string with asyncpg driver (e.g., `postgresql+asyncpg://postgres:postgres@localhost:5432/marketintel`).
- `CORS_ORIGINS`: Comma-separated list of permitted origins (default: `http://localhost:3000,http://127.0.0.1:3000`).

---

## 3. Backend Setup & Startup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   pytest -v
   ```

5. Start the backend server:
   ```bash
   python run.py
   ```
   Or via Uvicorn CLI:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. Verify API health:
   - Health check: `http://localhost:8000/api/v1/health`
   - Readiness check: `http://localhost:8000/api/v1/health/ready`
   - Interactive Swagger docs: `http://localhost:8000/docs`

---

## 4. Frontend Setup & Startup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start Next.js development server:
   ```bash
   npm run dev
   ```

4. Open the browser:
   Visit `http://localhost:3000` to access the MarketIntel AI dashboard.

5. Build for production:
   ```bash
   npm run build
   npm run start
   ```

---

## 5. PostgreSQL Database Setup (Optional for Phase 1)

If you have a local PostgreSQL instance:
```sql
CREATE DATABASE marketintel;
```

Run database migrations via Alembic:
```bash
cd backend
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

If PostgreSQL is not running, the application gracefully reports `"status": "degraded"` on `/api/v1/health/ready` while the main `/api/v1/health` endpoint remains completely functional.

