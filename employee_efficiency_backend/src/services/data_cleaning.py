import os
import pandas as pd
from sqlalchemy.orm import Session

from src.core.models import Dataset


def _load_df(dataset: Dataset) -> pd.DataFrame:
    if not os.path.exists(dataset.stored_path):
        raise ValueError("Dataset file not found")
    return pd.read_csv(dataset.stored_path)


# PUBLIC_INTERFACE
def clean_dataset(dataset_id: int, db: Session) -> dict:
    """Drop rows/cols with all-NaNs, save back to disk, and return stats."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    df = _load_df(dataset)
    before_rows, before_cols = df.shape
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")
    df.to_csv(dataset.stored_path, index=False)

    after_rows, after_cols = df.shape
    dataset.rows = after_rows
    dataset.cols = after_cols
    db.add(dataset)
    db.commit()

    return {
        "dataset_id": dataset.id,
        "removed_rows": before_rows - after_rows,
        "removed_cols": before_cols - after_cols,
        "message": "Cleaning complete",
    }
