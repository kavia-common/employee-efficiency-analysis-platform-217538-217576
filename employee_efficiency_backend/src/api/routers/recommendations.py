from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.schemas import RecommendationsResponse
from src.services.recommendations import get_recommendations

router = APIRouter(tags=["Recommendations"])


# PUBLIC_INTERFACE
@router.get("", response_model=RecommendationsResponse, summary="Get recommendations")
def recommendations(dataset_id: int, db: Session = Depends(get_db)):
    """Return recommendations for the dataset based on EDA, ANOVA, and clusters."""
    try:
        items = get_recommendations(dataset_id, db)
        return RecommendationsResponse(dataset_id=dataset_id, items=items)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
