from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import Base, engine
from .routers_auth import router as auth_router
from .routers_orders import router as orders_router
from .routers_returns import router as returns_router
from .routers_recommendations import router as recommendations_router

settings = get_settings()

app = FastAPI(
    title="E-commerce Backend API",
    description="REST API for orders, returns, recommendations, and authentication. Optional Supabase JWT verification.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "User registration, login and profile."},
        {"name": "Orders", "description": "Endpoints to query and manage orders."},
        {"name": "Returns", "description": "Return policies and return requests."},
        {"name": "Recommendations", "description": "Personalized recommendations."},
        {"name": "Health", "description": "Service health checks."},
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables (for demo purposes; in production use migrations)
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"], summary="Health Check", description="Simple service liveness check.")
def health_check():
    """Return service health indicator."""
    return {"message": "Healthy"}


# Include routers
app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(returns_router)
app.include_router(recommendations_router)
