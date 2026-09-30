from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import make_asgi_app
from sqlalchemy import text

from backend.api.app import models
from backend.api.app.database import Base, SessionLocal, engine
from backend.api.app.metrics import metrics_middleware
from backend.api.app.routers.orders import router as orders_router
from backend.api.app.routers.products import router as products_router


app = FastAPI(
    title="CloudCart API",
    version="1.0.0",
)


Base.metadata.create_all(
    bind=engine
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(
    metrics_middleware
)


@app.get("/")
def root():
    return {
        "service": "cloudcart-api",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health/live")
def liveness():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness():
    db = SessionLocal()

    try:
        db.execute(
            text("SELECT 1")
        )

        return {
            "status": "ready",
            "database": "connected",
        }

    finally:
        db.close()


app.include_router(
    products_router
)

app.include_router(
    orders_router
)


metrics_app = make_asgi_app()

app.mount(
    "/metrics",
    metrics_app,
)
