import os
import pandas as pd
from sqlalchemy.orm import Session
from scipy import stats

from src.core.models import Dataset, ANOVAResult


def _load_df(dataset: Dataset) -> pd.DataFrame:
    if not os.path.exists(dataset.stored_path):
        raise ValueError("Dataset file not found")
    return pd.read_csv(dataset.stored_path)


# PUBLIC_INTERFACE
def compute_anova(dataset_id: int, target: str, group_by: str, db: Session) -> dict:
    """Compute one-way ANOVA for the target variable across groups defined by group_by."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    df = _load_df(dataset)
    if target not in df.columns or group_by not in df.columns:
        raise ValueError("Specified columns not found in dataset")

    groups = [group[target].dropna().values for _, group in df.groupby(group_by)]
    if len(groups) < 2:
        raise ValueError("Not enough groups for ANOVA")

    f_stat, p_value = stats.f_oneway(*groups)

    result = {"f_stat": float(f_stat), "p_value": float(p_value), "group_by": group_by, "target": target}

    existing = db.query(ANOVAResult).filter(ANOVAResult.dataset_id == dataset.id).first()
    if existing:
        existing.result_json = result
    else:
        db.add(ANOVAResult(dataset_id=dataset.id, result_json=result))
    db.commit()

    return result
