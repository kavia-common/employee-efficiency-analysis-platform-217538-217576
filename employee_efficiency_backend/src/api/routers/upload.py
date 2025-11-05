import os
from typing import Tuple

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd

from src.core.db import get_db
from src.core.models import Dataset
from src.core.schemas import UploadResponse

router = APIRouter(tags=["Upload"])

DATA_DIR = os.getenv("DATA_DIR", "employee-efficiency-analysis-platform-217538-217576/employee_efficiency_backend/data")
os.makedirs(DATA_DIR, exist_ok=True)


def _save_uploaded_file(file: UploadFile) -> Tuple[str, pd.DataFrame]:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    path = os.path.join(DATA_DIR, file.filename)
    content = file.file.read()
    with open(path, "wb") as f:
        f.write(content)
    df = pd.read_csv(path)
    return path, df


# PUBLIC_INTERFACE
@router.post("", response_model=UploadResponse, summary="Upload dataset (CSV)")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a CSV dataset, store metadata, and return dataset id and shape."""
    stored_path, df = _save_uploaded_file(file)
    dataset = Dataset(filename=file.filename, stored_path=stored_path, rows=int(df.shape[0]), cols=int(df.shape[1]))
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return UploadResponse(dataset_id=dataset.id, filename=dataset.filename, rows=dataset.rows, cols=dataset.cols)
