from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.schemas import TrainRequest, TrainResponse, PredictRequest, PredictResponse
from src.services.modeling import train_model, predict_with_model

router = APIRouter(tags=["Model"])


# PUBLIC_INTERFACE
@router.post("/train", response_model=TrainResponse, summary="Train a model")
def train(req: TrainRequest, db: Session = Depends(get_db)):
    """Train a model with the selected algorithm and return metrics."""
    try:
        result = train_model(req.dataset_id, req.target, req.algorithm, db)
        return TrainResponse(dataset_id=req.dataset_id, algorithm=req.algorithm, metrics=result["metrics"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


# PUBLIC_INTERFACE
@router.post("/predict", response_model=PredictResponse, summary="Predict with trained model")
def predict(req: PredictRequest, db: Session = Depends(get_db)):
    """Predict using the last trained model for the dataset."""
    try:
        preds = predict_with_model(req.model_dataset_id, req.rows, db)
        return PredictResponse(predictions=preds)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
