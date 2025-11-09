# E-commerce Backend

FastAPI backend providing authentication, orders, returns, and recommendations.

## Setup

1. Create a `.env` file based on `.env.example` and set:
   - DATABASE_URL
   - JWT_SECRET
   - ACCESS_TOKEN_EXPIRE_MINUTES
   - ALLOW_ORIGINS
   - Optionally: SUPABASE_URL, SUPABASE_JWT_SECRET

2. Install dependencies:
   pip install -r requirements.txt

3. Run the server:
   uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

OpenAPI docs at /docs. The server initializes tables automatically for development.
