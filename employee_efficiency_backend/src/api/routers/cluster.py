from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.schemas import ClusterRequest, ClusterResponse
from src.services.clustering import run_kmeans

router = APIRouter(tags=["Cluster"])


# PUBLIC_INTERFACE
@router.post("/run", response_model=ClusterResponse, summary="Run K-Means clustering")
def run_cluster(req: ClusterRequest, db: Session = Depends(get_db)):
    """Run K-Means clustering and return labels and centers."""
    try:
        result = run_kmeans(req.dataset_id, req.n_clusters, db)
        return ClusterResponse(
            dataset_id=req.dataset_id,
            n_clusters=result["n_clusters"],
            labels=result["labels"],
            centers=result["centers"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
