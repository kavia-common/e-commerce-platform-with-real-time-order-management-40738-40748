# E-commerce Backend

FastAPI backend providing authentication, orders, returns, and recommendations.

## Setup

1) Environment
- Create a `.env` file based on `.env.example` and set:
  - DATABASE_URL (e.g., postgresql://appuser:dbuser123@localhost:5000/myapp)
  - JWT_SECRET (change this for non-dev)
  - ACCESS_TOKEN_EXPIRE_MINUTES (e.g., 60)
  - ALLOW_ORIGINS (include http://localhost:3000 for the React app)
  - Optional: SUPABASE_URL, SUPABASE_JWT_SECRET

2) Install dependencies
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt

3) Run the server
- uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

4) API docs
- Open http://localhost:3001/docs

Notes:
- The server creates tables automatically for development via SQLAlchemy models.
- Ensure your database is available (see ecommerce_database README for starting Postgres and running migrations).
- CORS is configured from ALLOW_ORIGINS and should include the frontend origin (http://localhost:3000).

### Quick verification flow
- Ensure database is ready and seeded:
  psql postgresql://appuser:dbuser123@localhost:5000/myapp -f ../ecommerce_database/startup.sql
- Start backend on :3001
- Use /auth/register then /auth/login to obtain token and call /orders, /returns, /recommendations with Authorization: Bearer <token>.
