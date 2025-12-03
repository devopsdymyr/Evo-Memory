"""FastAPI application main file."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.api.v1.endpoints import router as v1_router

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Evo-Memory Financial Services API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
        "endpoints": {
            "solve": "POST /api/v1/solve",
            "risk": "POST /api/v1/risk",
            "compliance": "POST /api/v1/compliance",
            "fraud": "POST /api/v1/fraud",
            "portfolio": "POST /api/v1/portfolio",
            "stats": "GET /api/v1/stats",
            "memories": "GET /api/v1/memories"
        }
    }

