from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.schemas import ANOVAResponse
from src.services.anova import compute_anova

router = APIRouter(tags=["ANOVA"])


# PUBLIC_INTERFACE
@router.get("", response_model=ANOVAResponse, summary="Run ANOVA test")
def get_anova(dataset_id: int, target: str, group_by: str, db: Session = Depends(get_db)):
    """Run one-way ANOVA on target by group_by."""
    try:
        res = compute_anova(dataset_id, target, group_by, db)
        return ANOVAResponse(dataset_id=dataset_id, results=res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
