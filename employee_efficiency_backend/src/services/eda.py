import os
import pandas as pd
from sqlalchemy.orm import Session

from src.core.models import Dataset, EDAResult


def _load_df(dataset: Dataset) -> pd.DataFrame:
    if not os.path.exists(dataset.stored_path):
        raise ValueError("Dataset file not found")
    return pd.read_csv(dataset.stored_path)


# PUBLIC_INTERFACE
def compute_eda(dataset_id: int, db: Session) -> dict:
    """Compute numeric column summary statistics and categorical counts."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    df = _load_df(dataset)

    summary = {
        "shape": {"rows": int(df.shape[0]), "cols": int(df.shape[1])},
        "numeric_summary": df.describe(include="number").fillna(0).to_dict(),
        "categorical_counts": {col: df[col].value_counts(dropna=False).to_dict() for col in df.select_dtypes(include=["object"]).columns},
        "columns": list(df.columns),
    }

    existing = db.query(EDAResult).filter(EDAResult.dataset_id == dataset.id).first()
    if existing:
        existing.summary_json = summary
    else:
        db.add(EDAResult(dataset_id=dataset.id, summary_json=summary))
    db.commit()

    return summary
