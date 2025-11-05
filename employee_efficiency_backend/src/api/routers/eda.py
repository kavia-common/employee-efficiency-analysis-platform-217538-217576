from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.schemas import EDAResponse
from src.services.eda import compute_eda

router = APIRouter(tags=["EDA"])


# PUBLIC_INTERFACE
@router.get("", response_model=EDAResponse, summary="Get EDA summary")
def get_eda(dataset_id: int, db: Session = Depends(get_db)):
    """Compute and return basic EDA summary for a dataset."""
    try:
        res = compute_eda(dataset_id, db)
        return EDAResponse(dataset_id=dataset_id, summary=res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
