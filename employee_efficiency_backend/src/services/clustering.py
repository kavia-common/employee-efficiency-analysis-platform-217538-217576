import os
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans

from src.core.models import Dataset, ClusterResult


def _load_df(dataset: Dataset) -> pd.DataFrame:
    if not os.path.exists(dataset.stored_path):
        raise ValueError("Dataset file not found")
    return pd.read_csv(dataset.stored_path)


# PUBLIC_INTERFACE
def run_kmeans(dataset_id: int, n_clusters: int, db: Session) -> dict:
    """Run KMeans on numeric features, store labels and centers."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    df = _load_df(dataset).dropna()
    X = df.select_dtypes(include="number")
    if X.shape[0] == 0 or X.shape[1] == 0:
        raise ValueError("No numeric data for clustering")

    model = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
    labels = model.fit_predict(X)
    centers = model.cluster_centers_.tolist()

    existing = db.query(ClusterResult).filter(ClusterResult.dataset_id == dataset.id).first()
    payload = {"labels": labels.tolist(), "centers": centers}
    if existing:
        existing.n_clusters = n_clusters
        existing.labels_json = {"labels": payload["labels"]}
        existing.centers_json = {"centers": payload["centers"]}
    else:
        db.add(ClusterResult(dataset_id=dataset.id, n_clusters=n_clusters,
                             labels_json={"labels": payload["labels"]},
                             centers_json={"centers": payload["centers"]}))
    db.commit()

    return {"n_clusters": n_clusters, **payload}
