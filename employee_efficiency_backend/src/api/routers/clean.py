from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.schemas import CleanResponse
from src.services.data_cleaning import clean_dataset

router = APIRouter(tags=["Cleaning"])


# PUBLIC_INTERFACE
@router.post("", response_model=CleanResponse, summary="Clean dataset (remove nulls)")
def clean_endpoint(dataset_id: int, db: Session = Depends(get_db)):
    """Perform simple cleaning: drop rows/cols with all-NaNs."""
    try:
        res = clean_dataset(dataset_id, db)
        return CleanResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
