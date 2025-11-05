from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from src.core.db import init_db
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

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB (creates tables if not exist)
init_db()

# PUBLIC_INTERFACE
@app.get("/", summary="Health Check", tags=["Upload"])
def health_check():
    """Health endpoint to verify service is up."""
    return {"message": "Healthy"}

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
