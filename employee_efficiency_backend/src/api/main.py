import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.core.db import init_db, get_db
from src.api.routers.upload import router as upload_router
from src.api.routers.clean import router as clean_router
from src.api.routers.eda import router as eda_router
from src.api.routers.anova import router as anova_router
from src.api.routers.model import router as model_router
from src.api.routers.cluster import router as cluster_router
from src.api.routers.recommendations import router as recs_router
from src.api.routers.report import router as report_router

openapi_tags = [
    {"name": "Upload", "description": "Endpoints to upload employee datasets."},
    {"name": "Cleaning", "description": "Data cleaning and preprocessing operations."},
    {"name": "EDA", "description": "Exploratory data analysis endpoints."},
    {"name": "ANOVA", "description": "Statistical testing (ANOVA)."},
    {"name": "Model", "description": "Model training and prediction APIs."},
    {"name": "Cluster", "description": "Clustering operations."},
    {"name": "Recommendations", "description": "Automated recommendations."},
    {"name": "Report", "description": "PDF report generation."},
]

app = FastAPI(
    title="Employee Efficiency Analysis Backend",
    description="APIs for data upload, cleaning, EDA, ANOVA, modeling, clustering, recommendations, and PDF report.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# CORS for frontend (allow both localhost and 127.0.0.1, overridable via env)
default_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
env_origins = os.getenv("CORS_ALLOW_ORIGINS")
allow_origins = [o.strip() for o in env_origins.split(",")] if env_origins else default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB (creates tables if not exist)
init_db()

# PUBLIC_INTERFACE
@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    """Health endpoint to verify service is up."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get(
    "/health/db",
    summary="Database Health Check",
    description="Checks if the application can connect to the configured PostgreSQL database and run a simple query.",
    tags=["Health"],
)
def db_health_check(db: Session = Depends(get_db)):
    """Attempt a simple SELECT 1 to validate DB connectivity."""
    try:
        db.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}

# Optional route noting WebSocket (not used but documented for completeness)
# PUBLIC_INTERFACE
@app.get(
    "/docs/websocket",
    response_class=PlainTextResponse,
    summary="WebSocket usage (not applicable)",
    tags=["Upload"],
)
def websocket_help():
    """This project uses REST endpoints only. No WebSocket endpoints are provided."""
    return "No websocket endpoints available."

# Include routers
app.include_router(upload_router, prefix="/upload")
app.include_router(clean_router, prefix="/clean")
app.include_router(eda_router, prefix="/eda")
app.include_router(anova_router, prefix="/anova")
app.include_router(model_router, prefix="/model")
app.include_router(cluster_router, prefix="/cluster")
app.include_router(recs_router, prefix="/recommendations")
app.include_router(report_router, prefix="/report")
