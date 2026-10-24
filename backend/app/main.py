from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import public_router, router
from .config import settings
from .core.rate_limit import RateLimitMiddleware
from .db.session import init_db
from .graph.client import get_graph
from .rag.store import get_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    get_store()   # warm the FAISS index
    get_graph()   # connect to Neo4j (or fall back to in-memory graph)
    yield


app = FastAPI(
    title="Autonomous Fraud Investigation System",
    description="Agentic RAG + Graph ML fraud investigation backend",
    version="1.0.0",
    lifespan=lifespan,
)

cors_origins_list = (
    [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    if settings.cors_origins != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True if "*" not in cors_origins_list else False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, limit=240, window_seconds=60)


@public_router.get("/")
def root():
    """Root endpoint for deployment verification."""
    return {
        "status": "online",
        "service": "Autonomous Fraud Investigation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


app.include_router(public_router)
app.include_router(router)
